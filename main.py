from fastapi import FastAPI

from agent import get_agent

app = FastAPI(title="AI Agent")
agent = get_agent()


@app.get("/history/{thread_id}")
async def get_chat_history(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}

    # 从检查点获取当前状态快照
    state = agent.get_state(config)

    # 如果该线程从未运行过，state.values 会是空的
    if not state.values or "messages" not in state.values:
        return {"thread_id": thread_id, "messages": [], "status": "no_history"}

    # 提取并格式化消息列表
    messages = [
        {
            "role": msg.type,  # 'human', 'ai', 'system' 等
            "content": msg.content,
            "timestamp": msg.response_metadata.get("created_at", None),  # 如果有的话
        }
        for msg in state.values["messages"]
    ]

    return {"thread_id": thread_id, "messages": messages}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)