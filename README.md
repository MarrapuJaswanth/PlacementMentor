# PlacementMentor

Ready-to-run AI placement preparation chatbot.

## Run
1. Install Python 3.10+
2. Create environment:
   `python -m venv .venv`
3. Activate it:
   Windows: `.venv\Scripts\activate`
4. Install:
   `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`
6. Add either a Groq or Gemini API key.
7. Start:
   `uvicorn app.main:app --reload`
8. Open http://127.0.0.1:8000

The chatbot supports student profiles, role analysis, learning roadmaps, interview preparation and mock interviews.
