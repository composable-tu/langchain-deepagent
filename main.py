import os
from pathlib import Path

import dotenv
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

dotenv.load_dotenv()

system_prompt = """Your interview skill file is located at: /skills/. 
Use this EXACT virtual path with read_file."""

baseChatModel: BaseChatModel = ChatOpenAI(
    temperature=0.6,
    model="GLM-4.5-Flash",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_URL"),
)

project_dir = Path(__file__).parent.absolute()

checkpointer = MemorySaver()

agent = create_deep_agent(
    model=baseChatModel,
    system_prompt=system_prompt,
    backend=FilesystemBackend(root_dir=project_dir.as_posix(), virtual_mode=True),
    skills=[(project_dir / "skills/").as_posix()],
    interrupt_on={
        "read_file": False,  # No interrupts needed
    },
    checkpointer=checkpointer,  # Required!
)

print(agent)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "你好，我是想来面试软件开发岗位，有 300 年经验，包括汇编语言、Basic、C、C++、Dart、Go、Java、JS、Kotlin、Pascal、R Lang、Rust、Scala、Swift、TypeScript。",
            }
        ]
    },
    config={"configurable": {"thread_id": "interview-session-001"}},
)

for message in result["messages"]:
    print(message.content)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "我会汇编语言、Basic、C、C++、Dart、Go、Java、JS、Kotlin、Pascal、R Lang、Rust、Scala、Swift、TypeScript。技术官，开始面试吧",
            }
        ]
    },
    config={"configurable": {"thread_id": "interview-session-001"}},
)

for message in result["messages"]:
    print(message.content)
