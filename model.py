from pydantic import BaseModel
from typing import Optional

class CodeSnippet(BaseModel):
    language: str
    code: str

class BugReport(BaseModel):
    language: str
    bug_type: str
    description: str
    suggestion: Optional[str]
