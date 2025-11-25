from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend (Wix) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    # Note: when running in production, fail fast and surface an informative error
    raise RuntimeError("OPENAI_API_KEY is not set in the environment. Set it in `.env` or the environment variables.")

client = OpenAI(api_key=OPENAI_KEY)

@app.post("/chat")
async def chat(payload: dict):
    question = payload.get("message", "")
    if not question:
        raise HTTPException(status_code=400, detail="`message` is required in the payload")

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "Du er NettJus AI. Svar kort, presist og juridisk forsiktig."},
                {"role": "user", "content": question},
            ],
            # Optional: tune response length
            max_tokens=500,
        )

        # The response structure depends on the OpenAI client version; this matches the
        # `openai` client that returns choices with a `message` mapping.
        answer = None
        if hasattr(response, "choices") and len(response.choices) > 0:
            # choices[0].message may be a mapping or object depending on the SDK
            first = response.choices[0]
            if isinstance(first.message, dict):
                answer = first.message.get("content")
            else:
                # fallback to attribute access
                answer = getattr(first.message, "content", None)

        if not answer:
            raise ValueError("No answer returned from OpenAI")

        return {"answer": answer}

    except Exception as e:
        # Log the exception in real apps. Return a safe error to the client.
        raise HTTPException(status_code=500, detail=f"OpenAI request failed: {str(e)}")
