from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages

class BirthDetails(TypedDict):
    name: str
    date: str        # YYYY-MM-DD
    time: str        # HH:MM
    place: str
    latitude: Optional[float]
    longitude: Optional[float]
    timezone: Optional[str]

class AgentState(TypedDict):
    # Chat messages — add_messages handles appending automatically
    messages: Annotated[list, add_messages]
    
    # User birth details
    birth_details: Optional[BirthDetails]
    
    # Computed birth chart — stored so we don't recompute
    birth_chart: Optional[dict]
    
    # Today's transits
    daily_transits: Optional[dict]
    
    # What kind of question is this?
    intent: Optional[str]  # "chart_request" | "daily_horoscope" | "general_question"
    
    # Tool outputs for current turn
    tool_outputs: Optional[dict]
    
    # Safety flag
    is_safe: Optional[bool]