from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode , tools_condition
from langchain_core.tools import tool
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
)

client = MultiServerMCPClient(
    {
        "arith":{
            "transport":"stdio",
            "command":"python3",
            "args":["C:\Users\Krishna gupta\OneDrive\Desktop\MATH-MCP-SERVER/main.py"]
        }
    }
)


# state
class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]


def build_graph():

    # nodes
    async def chat_node(state:ChatState):
    
        messages = state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {'messages':[response]}
    
    tool_node = ToolNode(tools)
    
    
    # defining graph and nodes 
    graph = StateGraph(ChatState)
    
    graph.add_node("chat_node",chat_node)
    graph.add_node("tools",tool_node)
    
    # defining graph connections
    graph.add_edge(START,"chat_node")
    graph.add_conditional_edges("chat_node",tools_condition)
    graph.add_edge("tools","chat_node")
    
    chatbot = graph.compile()
    return chatbot

async def main():
    chatbot = build_graph()

    # running the graph
    result = await chatbot.ainvoke({"messages":[HumanMessage(content="Find the modulus of 123456 and 23 and give answer like a cricketer commnetator.")]})

    print(result['messages'][-1].content)


if __name__ == "__main__":
    asyncio.run(main())