# RAG Basic Experiment

一个基于 LangChain 和 DeepSeek API 的 RAG 实验项目。

## 功能特点

- 支持基于文档的问答（RAG）
- 支持直接与 LLM 对话
- 使用 BAAI 的嵌入模型
- 使用 DeepSeek 的 LLM
- 提供简单的 Web 界面

## 安装

1. 克隆项目
```bash
git clone [your-repo-url]
cd RAG-basic-exp
```

2. 安装依赖
```bash
pip3 install -r requirements.txt
```

3. 配置环境变量
创建 `.env` 文件并添加：
```
DEEPSEEK_API_KEY=your_api_key_here
BAAI_API_KEY=your_embedding_api_key_here
```

## 使用

1. 启动应用
```bash
python3 app.py
```

2. 访问 Web 界面
打开浏览器访问 http://127.0.0.1:7860

## 项目结构

```
.
├── app.py                 # 主应用
├── embedding/             # 嵌入模型相关
├── figures/              # 图片资源
├── knowledge_db/         # 知识库文档
├── llm_api/             # LLM API 相关
├── qa_chain/            # 问答链相关
└── requirements.txt     # 项目依赖
```

## 注意事项

- 确保 API Key 正确配置
- 知识库文档需要放在 knowledge_db 目录

## 参考链接

- [个人知识助手](https://github.com/logan-zou/Chat_with_Datawhale_langchain)
- [Deepseek API接口文档](https://api-docs.deepseek.com/zh-cn/)
- [知乎：选择bge-m3作为embedding模型](https://zhuanlan.zhihu.com/p/20939683190)
