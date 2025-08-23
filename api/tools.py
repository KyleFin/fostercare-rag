import os
from dotenv import load_dotenv
from langchain_cohere import CohereRerank
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import tool
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores import Qdrant
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from operator import itemgetter
from typing_extensions import List, TypedDict
from uuid import uuid4

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

projectUuid = f"Foster Care cert challenge - {uuid4().hex[0:8]}"
os.environ["LANGCHAIN_PROJECT"] = projectUuid
os.environ["LANGSMITH_PROJECT"] = projectUuid

os.environ["LANGCHAIN_TRACING_V2"] = "true"

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGCHAIN_TRACING_v2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com/"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com/"

from langchain.callbacks import LangChainTracer
from langchain.schema.runnable import RunnableConfig
tracer = LangChainTracer(project_name=os.environ["LANGSMITH_PROJECT"])

tavily_search_tool = TavilySearchResults(max_results=5)

# RAG tool
path = "./data/"
loader = DirectoryLoader(path, glob="pub5108.pdf", loader_cls=PyMuPDFLoader)    # glob = "*.pdf" to load all pdfs
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_documents = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Qdrant.from_documents(
    docs,
    embeddings,
    location=":memory:",
    collection_name="FosterCarePolicies"
)

naive_retriever = vectorstore.as_retriever(search_kwargs={"k" : 10})

def retrieve(state):
    retrieved_docs = naive_retriever.invoke(state["question"], {
        "tags" : ["RAG retrieve"],
        "callbacks": [tracer],
    })
    return {"context": retrieved_docs}

RAG_TEMPLATE = """\
You are a helpful and kind assistant. Use the context provided below to answer the question.

If you do not know the answer, or are unsure, say you don't know.

Query:
{question}

Context:
{context}
"""

rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
chat_model = ChatOpenAI(model="gpt-4.1-nano")

def generate(state):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = rag_prompt.format_messages(question=state["question"], context=docs_content)
    response = chat_model.invoke(messages, {
        "tags" : ["RAG Generate"],
        "callbacks": [tracer],
    })
    return {"response": response.content}

class State(TypedDict):
    question: str
    context: List[Document]
    response: str

graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

# response = graph.invoke({"question": ""})

# naive_retrieval_chain = (
#     # INVOKE CHAIN WITH: {"question" : "<<SOME USER QUESTION>>"}
#     # "question" : populated by getting the value of the "question" key
#     # "context"  : populated by getting the value of the "question" key and chaining it into the base_retriever
#     {"context": itemgetter("question") | naive_retriever, "question": itemgetter("question")}
#     # "context"  : is assigned to a RunnablePassthrough object (will not be called or considered in the next step)
#     #              by getting the value of the "context" key from the previous step
#     | RunnablePassthrough.assign(context=itemgetter("context"))
#     # "response" : the "context" and "question" values are used to format our prompt object and then piped
#     #              into the LLM and stored in a key called "response"
#     # "context"  : populated by getting the value of the "context" key from the previous step
#     | {"response": rag_prompt | chat_model, "context": itemgetter("context")}
# )

compressor = CohereRerank(model="rerank-v3.5")
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=naive_retriever
)

contextual_compression_retrieval_chain = (
    {"context": itemgetter("question") | compression_retriever, "question": itemgetter("question")}
    | RunnablePassthrough.assign(context=itemgetter("context"))
    | {"response": rag_prompt | chat_model, "context": itemgetter("context")}
)

@tool
def fostercare_rag_tool(question: str) -> str:
    """Useful for when you need to answer questions about foster care policies. Input should be a fully formed question."""
    # response = graph.invoke({"question": question}, {
    response = contextual_compression_retrieval_chain.invoke({"question": question}, {
        "tags" : ["Contextual retriever"],
        "callbacks": [tracer],
    })
    return {
        # "messages": [HumanMessage(content=response["response"])],
        "messages": [HumanMessage(content=response["response"].content)],
        "context": response["context"]
    }

tool_belt = [
    tavily_search_tool,
    fostercare_rag_tool,
]