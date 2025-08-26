from .agent import compiled_graph
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
    developer_message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        
        async def generate():
            inputs = {"messages": [
                SystemMessage(
                    content="""You are a helpful assistant that guides researchers to authoritative information about state foster care policies.
                    You answer questions based on provided context. You must only use the provided context, and cannot use your own knowledge.
                    You are ONLY allowed to perform web searches if the LATEST SystemMessage explicitly states that you are allowed to.
                    Prefer retrieving policy documents over checking the web.
                    You must cite sources for all statements. For RAG sources, include the original filepath and page number.
                    If you cannot answer the question with high accuracy, respond with "I don't know."
                    """
                ),
                SystemMessage(content=request.developer_message),
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