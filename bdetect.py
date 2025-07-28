import google.generativeai as genai
import os
import json

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Optional: Used internally if needed, but NOT registered as a route
def generation_function(language: str, code: str, mode:str) -> str:
    if mode == "developer-friendly":
        tone_instruction = "Explain in a technical and concise manner suitable for developers."
    else:
        tone_instruction = "Explain simply in a friendly tone suitable for beginners."

    prompt = f"{tone_instruction}\n\nFind bugs in this {language} code:\n\n{code}"
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text

def get_bug_report(language: str, code: str, mode:str) -> dict:
    response_text = generation_function(language, code, mode)
    prompt = f"""
You are an AI code reviewer. Analyze the following {language} code snippet.

Code:
    {code}
    
Identify:
- bug_type: One of ["Logical Bug", "Runtime Bug", "Off-by-One Error", "Edge-Case"]
- description: Explain what’s wrong in plain English. response_text
- suggestion: Suggest how to fix or improve it.

Respond only in JSON format.
"""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    try:
        import json
        return json.loads(response.text)
    except Exception as e:
        return {
            "bug_type": "Unknown",
            "description": "Could not parse LLM response.",
            "suggestion": "Check the prompt or model output format.",
        }

