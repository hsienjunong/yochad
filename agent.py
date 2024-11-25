from typing import Annotated
from typing_extensions import TypedDict
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition

import components.initializer as init
import tools.utilities as util
import tools.commands as commands

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}

llm = ChatOpenAI(model=init.DEFAULT_CHAT_MODEL)

assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are an advanced, intelligent assistant capable of understanding and interpreting complex natural language inputs from users. "
                "Your role is to act as an intermediary between human commands and the precise actions needed to fulfill them. "
                "You leverage state-of-the-art natural language processing techniques and have access to a suite of tools to assist in executing tasks.\n\n"
                "Your primary goals are:\n"
                "1. **Understanding User Intent:** Comprehend the user's query or command, including nuanced or context-dependent requests, while considering the broader context of the conversation and historical interactions.\n\n"
                "2. **Tool Selection and Execution:** Accurately determine which tools or resources to use based on the user's request.\n"
                "3. **Error Handling and Responsiveness:** If a command or request is ambiguous or does not lead to meaningful output:\n"
                "4. **Context Retention:** Keep track of conversation history and maintain continuity across interactions. Use prior messages to inform future responses where appropriate, ensuring a coherent and consistent conversation.\n\n"
                "5. **Accuracy and Clarity:** Strive to provide responses that are precise, actionable, and directly relevant to the user's needs. Avoid overcomplicating outputs and ensure clarity in every step.\n\n"
                "6. **UR3e Robotics Expertise:** Be particularly adept at understanding robotic workflows, URScript syntax, and operational constraints for the UR3e robot. Ensure any robotic commands are syntactically correct, logically valid, and safe to execute.\n\n"
            ),
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now())


tools = [
    TavilySearchResults(max_results=1),
    commands.send_command_to_robot,
    commands.generate_urscript,
]

assistant_runnable = assistant_prompt | llm.bind_tools(tools)

builder = StateGraph(State)
builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("tools", util.create_tool_node_with_fallback(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

