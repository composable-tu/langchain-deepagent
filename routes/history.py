from fastapi import APIRouter

from agent import get_agent

router = APIRouter()

@router.get("/history/{thread_id}")
async def get_chat_history(thread_id: str):
    """
    获取指定线程的聊天历史记录

    通过 thread_id 查询对应会话的完整消息记录，返回格式化的聊天历史数据。

    Args:
        thread_id (str): 线程ID，用于标识特定的会话

    Returns:
        dict: 包含以下字段的字典：
            - thread_id (str): 线程ID
            - messages (list): 完整的对话历史列表，每个消息包含：
                - role (str): 消息角色（"human" 或 "ai"）
                - content (str): 消息内容
            - has_finished (bool): 对话是否已结束
    """
    config = {"configurable": {"thread_id": thread_id}}

    # Agent 当前状态快照
    state = get_agent().get_state(config)

    # 如果该线程从未运行过，直接返回空列表
    if not state.values or "messages" not in state.values:
        return {"thread_id": thread_id, "messages": [], "status": "no_history"}

    has_finished = False
    for msg in state.values["messages"]:
        if msg.type == "tool" and msg.content == "INTERVIEW_FINISHED_SIGNAL":
            has_finished = True
            break

    messages = [
        {"role": msg.type, "content": msg.content} for msg in state.values["messages"]
    ]

    return {"thread_id": thread_id, "messages": messages, "has_finished": has_finished}
