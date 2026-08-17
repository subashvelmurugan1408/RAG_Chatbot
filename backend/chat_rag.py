from rag_chain import create_rag_chain

def main():
    print("🤖 RAG Chatbot - Ask me anything about the documents!")
    print("Type 'exit' to quit\n")
    
    chain = create_rag_chain()
    
    while True:
        question = input("\nYou: ").strip()
        
        if question.lower() == "exit":
            print("Goodbye! 👋")
            break
        
        if not question:
            continue
        
        print("\nBot: Thinking...", end="", flush=True)
        answer = chain.invoke(question)
        print(f"\r\nBot: {answer}")

if __name__ == "__main__":
    main()