from typing import Annotated, TypedDict, Literal 
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from server.schemas.code import CodingRequest
from server.utils.llm import chat_llm
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from server.settings import settings

class State(TypedDict):
    messages: Annotated[list, add_messages]
    language: str
    framework: str
    code_snippet: str
    description: str
    error_message: str
    complexity: Literal["basic", "intermediate", "advanced"]
    environment: str
    
async def extract_code_query_node(state: State):
    prompt = (
        """
            You are a helpful and experienced coding assistant. 
            Your goal is to help the user with coding-related tasks such as writing, fixing, explaining, or refactoring code. 
            Respond using clear, concise explanations and include code examples where relevant. 
            Adapt your response to the user's specified language, framework, and complexity level.

            User message: {user_message}
        """
    )

    user_message = state["messages"][-1].content
    formatted_prompt = prompt.format(user_message=user_message)
    llm = chat_llm.with_structured_output(CodingRequest)
    parsed = llm.invoke(formatted_prompt)

    updated_state = dict(state)
    updated_state["language"] = parsed.language
    updated_state["framework"] = parsed.framework
    updated_state["code_snippet"] = parsed.code_snippet
    updated_state["description"] = parsed.description
    updated_state["error_message"] = parsed.error_message
    updated_state["complexity"] = parsed.complexity
    updated_state["environment"] = parsed.environment

    return updated_state

async def generate_code_node(state: State):
    language = state["language"]
    description = state["description"]
    error_message = state["error_message"]
    complexity = state["complexity"]
    environment = state["environment"]

    user_prompt = (
        f"You are an expert coding assistant helping a user solve a programming problem.\n"
        f"The user is working with {language} code.\n"
        f"The task is described as: {description.strip()}.\n"
    )

    if error_message:
        user_prompt += f"The user encountered the following error: {error_message.strip()}.\n"
    else:
        user_prompt += "The user did not report any specific error.\n"

    user_prompt += f"The user has requested a solution appropriate for a {complexity.lower()}-level programmer.\n"

    if environment:
        user_prompt += f"The code is being developed in the following environment: {environment}.\n"
    else:
        user_prompt += "No specific environment was mentioned.\n"

    user_prompt += (
        "Provide a clear, structured solution including well-commented code.\n"
        "If necessary, explain key parts of the code or reasoning behind the solution.\n"
        "Use best practices and align with the user's skill level.\n"
    )
    
    async with MultiServerMCPClient(
           { 
               "chat": {
                "url": f"{settings.BACKEND_URL}/code/mcp",
                "transport": "streamable_http"                     
               }
           }
        ) as client:
            agent = create_react_agent(
                chat_llm,
                client.get_tools()
            )

            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_prompt}]}
            )
    
    updated_state = dict(state)
    updated_state["messages"] = response["messages"]
    return updated_state

graph_builder = StateGraph(State)

graph_builder.add_node("extractor", extract_code_query_node)
graph_builder.add_node("generator", generate_code_node)

graph_builder.add_edge(START, "extractor")
graph_builder.add_edge("extractor", "generator")
graph_builder.add_edge("generator", END)

graph = graph_builder.compile(
    checkpointer=MemorySaver()
)
