from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

class EnterpriseAgent:
    """Multi-step AI Agent for enterprise automation."""

    def __init__(self, tools: list):
        self.llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
        self.tools = tools
        self.llm_with_tools = self.llm.bind_tools(tools)
        self.graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph(AgentState)
        tool_node = ToolNode(self.tools)
        builder.add_node("agent", self._call_model)
        builder.add_node("tools", tool_node)
        builder.set_entry_point("agent")
        builder.add_conditional_edges("agent", self._should_continue)
        builder.add_edge("tools", "agent")
        return builder.compile()

    def _call_model(self, state: AgentState):
        response = self.llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def _should_continue(self, state: AgentState):
        last = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"
        return END

    def run(self, user_input: str):
        result = self.graph.invoke({"messages": [HumanMessage(content=user_input)]})
        return result["messages"][-1].content

