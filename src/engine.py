import os
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

# LangChain imports
from langchain_community.document_loaders import YoutubeLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()

# 1. Define the State
# This is the "memory" that gets passed between steps.
class NoteState(TypedDict):
    video_url: str
    transcript: Optional[str]
    notes: Optional[str]
    error: Optional[str]

# 2. Define the Nodes (The Workers)

def load_video_node(state: NoteState):
    """
    Worker 1: Fetches the transcript from YouTube.
    """
    print(f"--- Loading Video: {state['video_url']} ---")
    try:
        # Configuration: language=["en"] ensures we get English captions
        loader = YoutubeLoader.from_youtube_url(
            state["video_url"],
            add_video_info=False,
            language=["en", "en-US", "en-GB"]
        )
        docs = loader.load()

        # Join all transcript parts into one big string
        full_transcript = "\n\n".join([d.page_content for d in docs])

        # Update state
        return {"transcript": full_transcript, "error": None}

    except Exception as e:
        return {"error": str(e), "transcript": None}

def generate_notes_node(state: NoteState):
    """
    Worker 2: Sends transcript to LLM to generate notes.
    """
    print("--- Generating Notes ---")

    # If previous step failed, stop here
    if state.get("error"):
        return {"notes": "Error occurred during video loading."}

    # Initialize Model (GPT-4o)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    # Define the Prompt
    system_prompt = """You are an expert technical writer and student.
    Your task is to create comprehensive, structured study notes from the provided video transcript.

    Rules:
    1. Use clear Markdown formatting (## Headings, * Bullet points).
    2. Extract key concepts, definitions, and code snippets if present.
    3. Keep it concise but do not lose important details.
    4. If the content is technical, capture specific commands or libraries mentioned.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Transcript:\n\n{transcript}")
    ])

    # Create the chain: Prompt -> LLM -> String Output
    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"transcript": state["transcript"]})

    return {"notes": response}

# 3. Build the Graph (The Assembly Line)

workflow = StateGraph(NoteState)

# Add nodes
workflow.add_node("loader", load_video_node)
workflow.add_node("writer", generate_notes_node)

# Add edges (connect the nodes)
# Start -> Loader -> Writer -> End
workflow.set_entry_point("loader")
workflow.add_edge("loader", "writer")
workflow.add_edge("writer", END)

# Compile the graph
engine = workflow.compile()