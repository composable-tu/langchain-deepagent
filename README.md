# LangChain Deep Agent 项目

> [!note]
> 该项目需要您持有兼容 OpenAI API 返回格式的云端大模型 API 地址和 API Key。
> 
> 推荐使用智谱平台，该平台提供的部分模型为免费模型：
> - 智谱国内版：https://bigmodel.cn/
> - 智谱国际版：https://z.ai/subscribe

## 第一次使用？

`uv` 是 Open WebUI 推荐的 Python 包管理器。请先参考 `uv` 官网安装 `uv` Python 包管理器：https://docs.astral.sh/uv/getting-started/installation/

然后，转到该项目，在根目录启动终端并运行以下命令以安装项目依赖：

```bash
uv sync
```

## 启动项目

请确保 Python 版本为 Python 3.11。过高或过低的 Python 版本可能存在问题。

请先将 `example.env` 文件改名为 `.env` 文件，然后运行以下命令以 `.env` 环境变量启动项目：

```bash
uv run main.py
```

然后可在控制台看到运行效果。

## 参考

- `uv` 文档：https://docs.astral.sh/uv/
- LangChain Deep Agent 文档：https://docs.langchain.com/oss/python/deepagents/