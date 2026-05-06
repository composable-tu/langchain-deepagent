from fastapi import HTTPException
from fastapi import APIRouter
from pydantic import BaseModel

from agent import get_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat/{thread_id}")
async def post_chat(thread_id: str, request: ChatRequest):
    """
    处理用户聊天请求并返回 AI 响应

    接收用户消息，调用 Agent 进行处理，返回完整的对话历史。
    支持基于 thread_id 的多轮对话上下文管理。

    Args:
        thread_id (str): 线程ID，用于标识和追踪特定的会话
        request (ChatRequest): 用户发送的消息内容

    Returns:
        dict: 包含以下字段的字典：
            - thread_id (str): 线程ID
            - messages (list): 完整的对话历史列表，每个消息包含：
                - role (str): 消息角色（"human" 或 "ai"）
                - content (str): 消息内容
            - has_finished (bool): 对话是否已结束
    """
    try:
        config = {"configurable": {"thread_id": thread_id}}

        result = get_agent().invoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config=config
        )

        has_finished = False
        for msg in result["messages"]:
            if msg.type == "tool" and msg.content == "INTERVIEW_FINISHED_SIGNAL":
                has_finished = True
                break

        messages = [
            {"role": msg.type, "content": msg.content}
            for msg in result["messages"]
        ]

        return {"thread_id": thread_id, "messages": messages, "has_finished": has_finished}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


