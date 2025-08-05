from agent import compiled_graph
from langchain_core.messages import HumanMessage, SystemMessage
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="Foster Care Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")    

class ChatRequest(BaseModel):
    user_message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        
        async def generate():
            inputs = {"messages": [
                SystemMessage(
                    content="You are a helpful assistant that guides foster care researchers to authoritative information about state policies. Prefer retrieving policy documents and checking the web for recent updates over your own knowledge. You must cite sources for all statements."
                ),
                HumanMessage(content=request.user_message),
                ]}
            result = ''
            async for chunk in compiled_graph.astream(inputs, stream_mode="updates"):
                for node, values in chunk.items():
                    print(f"Receiving update from node: '{node}")
                    if node == "action":
                        print(f"Tool used: {values['messages'][-1].name}")
                    print(values["messages"])
                    print("\n\n")
                    result = values["messages"][-1].content
            yield result

        return StreamingResponse(generate(), media_type="text/plain")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)