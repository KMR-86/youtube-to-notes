import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 1. Load env vars
load_dotenv()

def test_connection():
    print("Testing OpenAI Connection...")

    # Initialize the Model
    try:
        llm = ChatOpenAI(model="gpt-4o-mini")

        # Send a simple message
        response = llm.invoke([HumanMessage(content="what is the capital of Bangladesh?")])

        print("\n✅ Success! OpenAI Responded:")
        print(f"Response: {response.content}")
        print("\nCheck your LangSmith project dashboard - you should see this run trace there!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Double check your OPENAI_API_KEY in the .env file.")

if __name__ == "__main__":
    test_connection()