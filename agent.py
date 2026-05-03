import os
import sqlite3
from pathlib import Path
from typing import Optional

import dotenv
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.state import CompiledStateGraph

dotenv.load_dotenv()

def finish_interview():
    """
    当你认为面试已经结束，或者可以得出最终结论时调用此函数。
    """
    return "INTERVIEW_FINISHED_SIGNAL"

_agent_instance: Optional[CompiledStateGraph] = None

def get_agent() -> CompiledStateGraph:
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = _create_agent()
    return _agent_instance

def _create_agent() -> CompiledStateGraph:

    system_prompt = """面试 Skill 文件位于：/skills/。
    请在调用 read_file 时使用完全相同的虚拟路径。
    当你认为面试已经结束，或者可以得出最终结论时，请调用 finish_interview 工具，然后输出你对面试者的详细评价。"""

    baseChatModel: BaseChatModel = ChatOpenAI(
        temperature=0.6,
        model="GLM-4.5-Flash",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_URL"),
    )

    project_dir = Path(__file__).parent.absolute()

    conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
    checkpointer = SqliteSaver(conn)

    agent: CompiledStateGraph = create_deep_agent(
        model=baseChatModel,
        system_prompt=system_prompt,
        backend=FilesystemBackend(root_dir=project_dir.as_posix(), virtual_mode=True),
        tools=[finish_interview],
        skills=[(project_dir / "skills/").as_posix()],
        interrupt_on={
            "read_file": False,
        },
        checkpointer=checkpointer,
    )

    return agent

get_agent()
