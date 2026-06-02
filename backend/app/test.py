from dotenv import load_dotenv
load_dotenv("../../.env")
from graph import astro_graph
from langchain_core.messages import HumanMessage

try:
    result = astro_graph.invoke({
        'messages': [HumanMessage(content='hello')],
        'birth_details': None,
        'birth_chart': None,
        'daily_transits': None,
        'intent': None,
        'tool_outputs': None,
        'is_safe': True
    })
    print("SUCCESS:", result['messages'][-1].content)
except Exception as e:
    print("ERROR:", str(e))