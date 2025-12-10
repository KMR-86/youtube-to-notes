import sys
import os

# Add the parent directory's 'src' folder to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from engine import engine
from dotenv import load_dotenv

load_dotenv()

# A short, technical video for testing (FastAPI intro)
TEST_URL = "https://www.youtube.com/watch?v=4aYVLpY5FYU"

def run_test():
    print("Starting Engine Test...")

    # Invoke the graph
    result = engine.invoke({"video_url": TEST_URL})

    if result.get("error"):
        print(f"❌ Error: {result['error']}")
    else:
        print("\n✅ Notes Generated Successfully!\n")
        print(result["notes"][:50000] + "...") # Print first 500 chars

if __name__ == "__main__":
    run_test()