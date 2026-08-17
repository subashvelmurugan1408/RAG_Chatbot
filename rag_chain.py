import os
from dotenv import load_dotenv

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from retriever import get_retriever

load_dotenv()

# Initialize Hugging Face LLM
llm = HuggingFaceEndpoint(
   repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.7,
    huggingfacehub_api_token=os.getenv("HF_TOKEN"),
)

chat_model = ChatHuggingFace(llm=llm)


# Create prompt template
template = """You are a helpful AI assistant.
Answer the following question based only on the provided context.

Context:
{context}

Question:
{question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)


# Build RAG chain
def create_rag_chain():

    retriever = get_retriever()

    chain = (
        {
            "context": retriever
            | (lambda docs: "\n\n".join(d.page_content for d in docs)),
            "question": lambda x: x
        }
        | prompt
        | chat_model
        | StrOutputParser()
    )

    return chain


# Test the RAG system
if __name__ == "__main__":

    chain = create_rag_chain()

    question = "What is artificial intelligence?"

    answer = chain.invoke(question)

    print(f"Question: {question}\n")
    print(f"Answer: {answer}")