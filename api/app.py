# from tools import contextual_compression_retrieval_chain
from agent import compiled_graph
from langchain_core.messages import HumanMessage, SystemMessage
# Import required FastAPI components for building the API
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
# Import Pydantic for data validation and settings management
from pydantic import BaseModel
# Import OpenAI client for interacting with OpenAI's API
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI application with a title
app = FastAPI(title="Foster Care Chat API")

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows the API to be accessed from different domains/origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin
    allow_credentials=True,  # Allows cookies to be included in requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers in requests
)

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")    

# Define the data model for chat requests using Pydantic
# This ensures incoming request data is properly validated
class ChatRequest(BaseModel):
    # developer_message: str  # Message from the developer/system
    user_message: str      # Message from the user
    # model: Optional[str] = "gpt-4.1-mini"  # Optional model selection with default
    # api_key: str       # OpenAI API key for authentication

# Define the main chat endpoint that handles POST requests
@app.post("/api/chat")
async def chat(request: ChatRequest):
    # TODO: Add agentic RAG+Tavily chain here (w/ adv retriever) watch Wiz demo 35:22 graph, 44:37, 45:41?, React, Loom video, merge PR and submit link to cert.md
    try:
        # Initialize OpenAI client with the provided API key
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        
        # Create an async generator function for streaming responses
        async def generate():
            # Create a streaming chat completion request
            # stream = client.chat.completions.create(
            #     model="gpt-4.1-mini",
            #     messages=[
            #         # {"role": "developer", "content": request.developer_message},
            #         {"role": "user", "content": request.user_message}
            #     ],
            #     stream=True  # Enable streaming response
            # )
            
            # Yield each chunk of the response as it becomes available
            # for chunk in stream:
            #     if chunk.choices[0].delta.content is not None:
            #         yield chunk.choices[0].delta.content
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
            # yield contextual_compression_retrieval_chain.invoke({"question" : request.user_message})["response"].content

        # Return a streaming response to the client
        return StreamingResponse(generate(), media_type="text/plain")
    
    except Exception as e:
        # Handle any errors that occur during processing
        raise HTTPException(status_code=500, detail=str(e))

# Define a health check endpoint to verify API status
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

# Entry point for running the application directly
if __name__ == "__main__":
    import uvicorn
    # Start the server on all network interfaces (0.0.0.0) on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)