# main.py
from fastapi import FastAPI, HTTPException, Request, Body, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import google.generativeai as genai


from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
#from slowapi.decorator import limiter as limit_decorator
from slowapi.extension import Limiter as SlowAPILimiter
from fastapi.responses import JSONResponse

from bdetect import get_bug_report
from model import CodeSnippet, BugReport

# Load environment variables
load_dotenv()

# Initialize app and limiter
app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Setup Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
MOCK_MODE = os.getenv("MOCK_MODE") == "true"

if API_KEY:
    genai.configure(api_key=API_KEY)

# Rate-limit handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please slow down."},
    )




# Actual /find-bug route
@limiter.limit("10/minute")
@app.post("/find-bug", response_model=BugReport)

def find_bug(request: Request, snippet: CodeSnippet, mode: str= Query("developer-friendly", enum=["developer-friendly", "casual"])):
    if not snippet.code.strip():
        raise HTTPException(status_code=400, detail="Code is empty.")

    if snippet.language.lower() != "python":
        raise HTTPException(status_code=400, detail="Only Python is supported right now.")

    if snippet.code.count("\n") > 30:
        raise HTTPException(status_code=400, detail="Code exceeds 30 lines.")

    try:
        if MOCK_MODE:
            return BugReport(
                language=snippet.language,
                bug_type="Mocked Bug",
                description="This is a mocked bug description.",
                suggestion="This is a mocked suggestion."
            )
        else:
            result = get_bug_report(snippet.language, snippet.code, mode)
            return BugReport(language=snippet.language, **result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sample-cases", response_model=List[BugReport])
def get_sample_cases(mode: str = Query("developer-friendly", enum=["developer-friendly", "casual"])):
    casual = mode == "casual"
    return [
        {
            "language": "python",
            "code": "def is_even(n): return n % 2 == 1",
            "bug_type": "Logical Bug",
            "description": (
                "Oops! This function says odd numbers are even. It should check if `n % 2 == 0`."
                if casual else
                "Returns True for odd numbers instead of even. Use `n % 2 == 0` instead."
            ),
            "suggestion": "Use `n % 2 == 0` instead."
        },
        {
            "language": "python",
            "code": "for i in range(1, len(arr)): print(arr[i])",
            "bug_type": "Off-by-One Error",
            "description": (
                "You're skipping the first item in the list. Starting from index 1 misses it."
                if casual else
                "Skips the first element of the array. Use `range(len(arr))` if you want all elements."
            ),
            "suggestion": "Use `range(len(arr))` instead."
        },
        {
            "language": "python",
            "code": "if x = 5:\n    print(x)",
            "bug_type": "Syntax Error",
            "description": (
                "Oops, you used `=` instead of `==`. One is for assignment, the other for comparison!"
                if casual else
                "Uses assignment `=` instead of comparison `==`. Use `if x == 5:` instead."
            ),
            "suggestion": "Use `if x == 5:` instead."
        },
        {
            "language": "python",
            "code": "return x / y",
            "bug_type": "Runtime Bug",
            "description": (
                "Watch out! If `y` is 0, this will crash your program."
                if casual else
                "May raise `ZeroDivisionError` if `y` is 0. Check for `y != 0` before dividing."
            ),
            "suggestion": "Check if `y != 0` before dividing."
        },
        {
            "language": "python",
            "code": "if not arr:\n    process(arr)",
            "bug_type": "Edge-Case Bug",
            "description": (
                "You're calling `process(arr)` even when the list is empty! That might not be what you want."
                if casual else
                "`process(arr)` is called even when `arr` is empty. Likely should be `if arr:` instead."
            ),
            "suggestion": "Use `if arr:` instead, or review logic."
        },
    ]
@app.get("/")
def read_root():
    return {"message": "Welcome to the BugFinder API! Use /find-bug to POST code for analysis."}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}


# if __name__ == "__main__":
#     import uvicorn
#     import os
#     port = int(os.environ.get("PORT", 8000))  # default to 8000 if running locally
#     uvicorn.run("main:app", host="0.0.0.0", port=port)

