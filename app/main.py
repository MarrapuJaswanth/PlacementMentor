import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
app=FastAPI(title="PlacementMentor")
STATIC=Path(__file__).parent/"static"
app.mount("/static",StaticFiles(directory=STATIC),name="static")

class Chat(BaseModel):
    message:str
    profile:dict={}
    mode:str="general"

SYSTEM='''You are PlacementMentor, an expert college placement coach.
Give practical, structured advice based on the student's profile.
Cover role responsibilities, technologies, important concepts, priority levels,
DSA, CS fundamentals, projects, resume, aptitude, technical interviews and HR.
For roadmaps adapt to the available preparation time.
For mock interviews ask one question at a time and evaluate the previous answer.
Do not invent company-specific facts.'''

def ask(prompt):
    provider=os.getenv("LLM_PROVIDER","groq").lower()
    if provider=="gemini":
        from google import genai
        c=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        r=c.models.generate_content(model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"),contents=prompt)
        return r.text
    from groq import Groq
    c=Groq(api_key=os.getenv("GROQ_API_KEY"))
    r=c.chat.completions.create(
        model=os.getenv("GROQ_MODEL","llama-3.3-70b-versatile"),
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":prompt}],
        temperature=0.4)
    return r.choices[0].message.content

@app.get("/")
def home(): return FileResponse(STATIC/"index.html")

@app.get("/health")
def health(): return {"status":"ok","provider":os.getenv("LLM_PROVIDER","groq")}

@app.post("/api/chat")
def chat(x:Chat):
    prompt=f"Student profile: {x.profile}\nMode: {x.mode}\nRequest: {x.message}"
    try: return {"answer":ask(prompt)}
    except Exception as e: return {"answer":f"API configuration error: {e}\nCheck your .env file and API key."}
