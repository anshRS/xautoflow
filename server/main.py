from fastapi import FastAPI
from .routers import auth, profile, chat, code
from server.mcps.code_mcp import code_mcp
import contextlib

# Create a combined lifespan to manage session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(code_mcp.session_manager.run()) 
        yield

app = FastAPI(lifespan=lifespan)

# MCP routes mounted
# app.mount("/chat", app=chatmcp.sse_app())
# app.mount("/chat", app=chat_mcp.streamable_http_app())
app.mount("/code", app=code_mcp.streamable_http_app())

# Application routes
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(chat.router)
app.include_router(code.router)

@app.get("/", status_code=200)
def root():
    return {"message": "Server Running"}

@app.get("/verify")
def welcome():
    return {"message": "Email verified successfully. Welcome!"}
