from pydantic import BaseModel, Field
from typing import Literal, Optional

class CodingRequest(BaseModel):
    language: Optional[str] = Field(
        "Python",
        description="The programming language involved in the task (e.g., 'Python', 'JavaScript')."
    )

    framework: Optional[str] = Field(
        None,
        description="The framework or library being used, if any (e.g., 'Django', 'React', 'FastAPI')."
    )

    code_snippet: Optional[str] = Field(
        None,
        description="A snippet of user-provided code related to the task."
    )

    description: str = Field(
        ...,
        description="A plain-language description of what the user wants the assistant to do."
    )

    error_message: Optional[str] = Field(
        None,
        description="The error message or traceback if the user is facing a bug or issue."
    )

    complexity: Literal["basic", "intermediate", "advanced"] = Field(
        "intermediate",
        description="The level of complexity the user expects in the code or explanation."
    ) 

    environment: Optional[str] = Field(
        None,
        description="The development environment in use (e.g., 'Jupyter Notebook', 'Linux terminal', 'VSCode')."
    )
    