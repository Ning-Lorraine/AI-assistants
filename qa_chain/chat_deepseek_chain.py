from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_api.deepseek_api import get_completion_deepseek
from qa_chain.get_vectordb import get_vectordb
import re
from pydantic import BaseModel, ConfigDict, Field
from pydantic_core import core_schema
from typing import Any, List, Tuple
import os
from pathlib import Path

# 获取项目根目录
ROOT_DIR = Path(__file__).parent.parent

# 设置数据库路径
DEFAULT_DB_PATH = str(ROOT_DIR / "knowledge_db")
DEFAULT_PERSIST_PATH = str(ROOT_DIR / "vector_db" / "chroma")

# 确保目录存在
os.makedirs(DEFAULT_DB_PATH, exist_ok=True)
os.makedirs(DEFAULT_PERSIST_PATH, exist_ok=True)

class Chat_Qa_Chain(BaseModel):
    """
    带历史记录的问答链类
    使用Pydantic进行数据验证和配置管理
    """
    model: str = Field(..., description="模型名称")
    temperature: float = Field(default=0.0, description="温度参数，控制输出的随机性")
    top_k: int = Field(default=4, description="检索返回的文档数量")
    chat_history: List[Tuple[str, str]] = Field(default_factory=list, description="对话历史记录")
    embedding_model: str = Field(default="BAAI/bge-large-zh-v1.5", description="嵌入模型名称")
    vectordb: Any = Field(default=None, description="向量数据库实例")
    chain: Any = Field(default=None, description="问答链实例")
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
        protected_namespaces=(),  # 解决命名冲突
        json_schema_mode="validation"  # 简化schema生成
    )
    

    def __init__(self, **data):
        """
        初始化问答链
        :param data: 配置参数
        """
        super().__init__(**data)
        self.vectordb = get_vectordb(DEFAULT_DB_PATH, DEFAULT_PERSIST_PATH)
        self.chain = self._create_chain()

    def _create_chain(self):
        """
        创建问答链
        :return: 配置好的问答链
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个有帮助的AI助手。"),
            ("human", "{question}")
        ])
        
        chain = prompt | self._get_llm() | StrOutputParser()
        return chain

    def _get_llm(self):
        """
        获取语言模型
        :return: 配置好的语言模型函数
        """
        return lambda x: get_completion_deepseek(
            model=self.model,
            prompt=x,
            temperature=self.temperature
        )

    def answer(self, question: str) -> str:
        """
        回答问题
        :param question: 用户问题
        :return: 模型回答
        """
        response = self.chain.invoke({"question": question})
        self.chat_history.append((question, response))
        return response

    def clear_history(self):
        """清除历史记录"""
        self.chat_history = []

    def change_history_length(self, history_len: int = 1):
        """
        保存指定对话轮次的历史记录
        :param history_len: 要保留的最近对话轮数
        :return: 截取后的历史记录
        """
        n = len(self.chat_history)
        return self.chat_history[n - history_len:]

    def answer_with_retrieval(self, question: str, temperature=None, top_k=4):
        """
        使用检索增强生成回答问题
        :param question: 用户问题
        :param temperature: 温度参数
        :param top_k: 检索返回的文档数量
        :return: 更新后的历史记录
        """
        if len(question) == 0:
            return "", self.chat_history
        
        llm = self._get_llm()
        
        retriever = self.vectordb.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": top_k}
        )

        qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever
        )

        result = qa({"question": question, "chat_history": self.chat_history})
        answer = result['answer']
        answer = re.sub(r"\\n", '<br/>', answer)
        
        self.chat_history.append((question, answer))

        return self.chat_history
