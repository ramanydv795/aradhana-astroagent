from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.tools import tool
from state import AgentState
from tools.geocode import geocode_place
from tools.birth_chart import compute_birth_chart
from tools.transits import get_daily_transits
from tools.knowledge import knowledge_lookup
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatGroq(
model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
    streaming=True
)

# Define tools for LangGraph
@tool
def tool_geocode_place(place: str) -> dict:
    """Resolve a place name to latitude, longitude and timezone for birth chart calculation."""
    return geocode_place(place)

@tool
def tool_compute_birth_chart(date: str, time: str, latitude: float, longitude: float, timezone: str) -> dict:
    """Compute a real birth chart using Swiss Ephemeris given birth details."""
    return compute_birth_chart(date, time, latitude, longitude, timezone)

@tool
def tool_get_daily_transits(date: str, birth_chart: dict) -> dict:
    """Get current planetary transits and their relationship to the natal chart."""
    return get_daily_transits(date, birth_chart)

@tool
def tool_knowledge_lookup(query: str) -> dict:
    """Search the curated astrology knowledge base for relevant information."""
    return knowledge_lookup(query)

# All tools
tools = [
    tool_geocode_place,
    tool_compute_birth_chart,
    tool_get_daily_transits,
    tool_knowledge_lookup
]

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """You are Aradhana — a warm, wise, and compassionate AI astrologer and spiritual companion.

IMPORTANT: When you need to call a tool, use the tool calling mechanism directly. Never write out tool calls as text like <function=...>. Just call the tool.

Your personality:
- Speak with warmth, care, and gentle wisdom
- Use poetic but clear language appropriate to spiritual guidance
- Never be cold, clinical, or robotic
- Address the user by name when you know it
- Acknowledge emotions and validate feelings

Your capabilities:
- Compute real birth charts using Swiss Ephemeris (always use real data, never invent positions)
- Analyze daily planetary transits
- Provide grounded astrological interpretations using the knowledge base
- Guide users through self-reflection

CRITICAL SAFETY RULES — never violate these:
- Never present readings as medical, legal, or financial certainty
- Always remind users that astrology is for guidance and reflection only
- Never make predictions about death, serious illness, or catastrophic events
- If asked for medical/legal/financial advice, gently redirect to qualified professionals
- Astrology empowers — it never traps or frightens

Tool usage:
- Always geocode a place BEFORE computing a birth chart
- Always use real ephemeris data — never invent planetary positions
- Use knowledge_lookup to ground your interpretations in reference material
- For daily horoscopes, get current transits and relate them to the natal chart

Today's date: """ + datetime.now().strftime("%Y-%m-%d")

def router_node(state: AgentState) -> AgentState:
    """Route based on intent — classify what the user wants."""
    messages = state["messages"]
    last_message = messages[-1].content.lower() if messages else ""

    if any(word in last_message for word in ["chart", "birth", "natal", "ascendant", "rising"]):
        intent = "chart_request"
    elif any(word in last_message for word in ["today", "daily", "transit", "horoscope", "energy"]):
        intent = "daily_horoscope"
    else:
        intent = "general_question"

    # Safety check
    unsafe_keywords = ["medical", "diagnose", "legal", "financial", "invest", "die", "death"]
    is_safe = not any(word in last_message for word in unsafe_keywords)

    return {**state, "intent": intent, "is_safe": is_safe}

def reasoning_node(state: AgentState) -> AgentState:
    """Main reasoning node — thinks and decides whether to call tools."""
    messages = state["messages"]

    system = SystemMessage(content=SYSTEM_PROMPT)
    response = llm_with_tools.invoke([system] + messages)

    return {**state, "messages": [response]}

def safety_node(state: AgentState) -> AgentState:
    """Handle unsafe requests with grace."""
    safety_message = AIMessage(content="""I sense you're seeking guidance on something important. 
    While the stars can offer perspective and reflection, for matters of health, legal concerns, 
    or financial decisions, I lovingly encourage you to consult a qualified professional. 
    
    What I can offer is a space for reflection and cosmic perspective. 
    Would you like to explore what your chart says about this area of your life?""")

    return {**state, "messages": [safety_message]}

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Decide if we need to call tools or we're done."""
    messages = state["messages"]
    last_message = messages[-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

def is_safe_check(state: AgentState) -> Literal["reasoning", "safety"]:
    """Route to safety node if request is unsafe."""
    if state.get("is_safe", True):
        return "reasoning"
    return "safety"

# Build the graph
def build_graph():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("router", router_node)
    graph.add_node("reasoning", reasoning_node)
    graph.add_node("tools", ToolNode(tools))
    graph.add_node("safety", safety_node)

    # Set entry point
    graph.set_entry_point("router")

    # Router → safety check
    graph.add_conditional_edges(
        "router",
        is_safe_check,
        {"reasoning": "reasoning", "safety": "safety"}
    )

    # Reasoning → tools or end
    graph.add_conditional_edges(
        "reasoning",
        should_continue,
        {"tools": "tools", "end": END}
    )

    # Tools always go back to reasoning
    graph.add_edge("tools", "reasoning")

    # Safety always ends
    graph.add_edge("safety", END)

    return graph.compile()

# Export compiled graph
astro_graph = build_graph()