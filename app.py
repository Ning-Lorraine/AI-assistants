# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# import gradio as gr
# from dotenv import load_dotenv, find_dotenv
# from llm_api.deepseek_api import get_completion_deepseek
# from qa_chain.chat_deepseek_chain import Chat_Qa_Chain
# import re

# # 加载环境变量
# _ = load_dotenv(find_dotenv())

# # 配置常量
# INIT_LLM = "deepseek-chat"
# EMBEDDING_MODEL = "BAAI/bge-large-zh-v1.5"
# DEFAULT_DB_PATH = "./knowledge_db"
# DEFAULT_PERSIST_PATH = "./vector_db/chroma"
# AIGC_AVATAR_PATH = "./figures/aigc_avatar.png"
# DATAWHALE_AVATAR_PATH = "./figures/datawhale_avatar.png"
# AIGC_LOGO_PATH = "./figures/aigc_logo.png"
# DATAWHALE_LOGO_PATH = "./figures/datawhale_logo.png"

# class ModelCenter():
#     def __init__(self):
#         self.qa_chains = {}

#     def get_qa_chain(self, model: str = INIT_LLM, temperature: float = 0.0, top_k: int = 4):
#         """获取或创建QA链"""
#         if model not in self.qa_chains:
#             self.qa_chains[model] = Chat_Qa_Chain(
#                 model=model,
#                 temperature=temperature,
#                 top_k=top_k,
#                 embedding_model=EMBEDDING_MODEL
#             )
#         return self.qa_chains[model]

#     def answer(self, question: str, chat_history: list = [], model: str = INIT_LLM, 
#               temperature: float = 0.3, top_k: int = 4):
#         """回答问题"""
#         if not question or len(question) < 1:
#             return "", chat_history
        
#         try:
#             chain = self.get_qa_chain(model, temperature, top_k)
#             response = chain.answer(question)
#             chat_history.append((question, response))
#             return "", chat_history
#         except Exception as e:
#             return str(e), chat_history

#     def clear_history(self):
#         """清除历史记录"""
#         self.qa_chains = {}

# def format_chat_prompt(message, chat_history):
#     """格式化聊天提示"""
#     prompt = ""
#     for turn in chat_history:
#         user_message, bot_message = turn
#         prompt = f"{prompt}\nUser: {user_message}\nAssistant: {bot_message}"
#     prompt = f"{prompt}\nUser: {message}\nAssistant:"
#     return prompt

# def respond(message, chat_history, model=INIT_LLM, temperature=0.1):
#     """生成回复"""
#     if not message or len(message) < 1:
#         return "", chat_history
    
#     try:
#         formatted_prompt = format_chat_prompt(message, chat_history)
#         bot_message = get_completion_deepseek(
#             model=model,
#             prompt=formatted_prompt,
#             temperature=temperature
#         )
#         bot_message = re.sub(r"\\n", '<br/>', bot_message)
#         chat_history.append((message, bot_message))
#         return "", chat_history
#     except Exception as e:
#         return str(e), chat_history

# # 创建模型中心实例
# model_center = ModelCenter()

# # 创建Gradio界面
# block = gr.Blocks()
# with block as demo:
#     with gr.Row(equal_height=True):           
#         gr.Image(value=AIGC_LOGO_PATH, scale=1, min_width=10, show_label=False, show_download_button=False, container=False)
#         with gr.Column(scale=2):
#             gr.Markdown("""<h1><center>RAG Basic Experiment</center></h1>""")
#         gr.Image(value=DATAWHALE_LOGO_PATH, scale=1, min_width=10, show_label=False, show_download_button=False, container=False)

#     with gr.Row():
#         with gr.Column(scale=4):
#             chatbot = gr.Chatbot(height=400, show_copy_button=True, show_share_button=True, 
#                                avatar_images=(AIGC_AVATAR_PATH, DATAWHALE_AVATAR_PATH))
#             msg = gr.Textbox(label="Prompt/问题")

#             with gr.Row():
#                 qa_btn = gr.Button("Chat with QA")
#                 clear = gr.ClearButton(components=[chatbot], value="Clear console")

#         with gr.Column(scale=1):
#             model_argument = gr.Accordion("参数配置", open=False)
#             with model_argument:
#                 temperature = gr.Slider(0, 1, value=0.01, step=0.01, 
#                                       label="Temperature", interactive=True)
#                 top_k = gr.Slider(1, 10, value=3, step=1, 
#                                 label="Top K", interactive=True)

#     # 设置按钮事件
#     qa_btn.click(
#         model_center.answer,
#         inputs=[msg, chatbot, gr.State(INIT_LLM), temperature, top_k],
#         outputs=[msg, chatbot]
#     )
    
    
#     msg.submit(
#         respond,
#         inputs=[msg, chatbot, temperature],
#         outputs=[msg, chatbot]
#     )
    
#     clear.click(model_center.clear_history)

#     gr.Markdown("""提醒：<br>
#     1. 使用中如果出现异常，将会在文本输入框进行展示，请不要惊慌。<br>
#     2. 点击Clear console可以清除历史记录。<br>
#     """)

# # 启动应用
# demo.launch() 


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import gradio as gr
from dotenv import load_dotenv, find_dotenv
from llm_api.deepseek_api import get_completion_deepseek
from qa_chain.chat_deepseek_chain import Chat_Qa_Chain
import re

# 加载环境变量
_ = load_dotenv(find_dotenv())

# 配置常量
INIT_LLM = "deepseek-chat"
EMBEDDING_MODEL = "BAAI/bge-large-zh-v1.5"
DEFAULT_DB_PATH = "./knowledge_db"
DEFAULT_PERSIST_PATH = "./vector_db/chroma"
AIGC_AVATAR_PATH = "./figures/aigc_avatar.png"
DATAWHALE_AVATAR_PATH = "./figures/datawhale_avatar.png"
AIGC_LOGO_PATH = "./figures/aigc_logo.png"
DATAWHALE_LOGO_PATH = "./figures/datawhale_logo.png"

class ModelCenter():
    def __init__(self):
        self.qa_chains = {}

    def get_qa_chain(self, model: str = INIT_LLM, temperature: float = 0.3, top_k: int = 4):
        """获取或创建QA链"""
        # if model not in self.qa_chains:
        #     try:
        #         self.qa_chains[model] = Chat_Qa_Chain(
        #             model=str(model),  # 确保model是字符串
        #             temperature=float(temperature),
        #             top_k=int(top_k),
        #             embedding_model=EMBEDDING_MODEL
        #         )
        #     except Exception as e:
        #         raise ValueError(f"创建QA链失败: {str(e)}")
        # return self.qa_chains[model]
        if model not in self.qa_chains:
            # 确保参数类型正确
            params = {
                "model": str(model),
                "temperature": float(temperature),
                "top_k": int(top_k),
                "embedding_model": str(EMBEDDING_MODEL)
            }
            try:
                self.qa_chains[model] = Chat_Qa_Chain.model_validate(params)
            except Exception as e:
                raise ValueError(f"Failed to create QA chain: {str(e)}")
        return self.qa_chains[model]

    def answer(self, question: str, chat_history: list = [], model: str = INIT_LLM, 
              temperature: float = 0.3, top_k: int = 4):
        """回答问题"""
        if not question or len(question) < 1:
            return "", chat_history
        
        try:
            # 参数验证
            model = str(model)
            temperature = float(temperature)
            top_k = int(top_k)
            
            chain = self.get_qa_chain(model, temperature, top_k)
            response = chain.answer(question)
            chat_history.append((question, response))
            return "", chat_history
        except Exception as e:
            error_msg = f"错误: {str(e)}"
            chat_history.append((question, error_msg))
            return "", chat_history

    def clear_history(self):
        """清除历史记录"""
        self.qa_chains = {}

def format_chat_prompt(message, chat_history):
    """格式化聊天提示"""
    prompt = ""
    for turn in chat_history:
        user_message, bot_message = turn
        prompt = f"{prompt}\nUser: {user_message}\nAssistant: {bot_message}"
    prompt = f"{prompt}\nUser: {message}\nAssistant:"
    return prompt

def respond(message, chat_history, temperature=0.1):
    """生成回复"""
    if not message or len(message) < 1:
        return "", chat_history
    
    try:
        formatted_prompt = format_chat_prompt(message, chat_history)
        bot_message = get_completion_deepseek(
            model=INIT_LLM,  # 使用默认模型
            prompt=formatted_prompt,
            temperature=float(temperature)
        )
        bot_message = re.sub(r"\\n", '<br/>', bot_message)
        chat_history.append((message, bot_message))
        return "", chat_history
    except Exception as e:
        error_msg = f"错误: {str(e)}"
        chat_history.append((message, error_msg))
        return "", chat_history

# 创建模型中心实例
model_center = ModelCenter()

# 创建Gradio界面
block = gr.Blocks()
with block as demo:
    with gr.Row(equal_height=True):           
        gr.Image(value=AIGC_LOGO_PATH, scale=1, min_width=10, show_label=False, show_download_button=False, container=False)
        with gr.Column(scale=2):
            gr.Markdown("""<h1><center>RAG Basic Experiment</center></h1>""")
        gr.Image(value=DATAWHALE_LOGO_PATH, scale=1, min_width=10, show_label=False, show_download_button=False, container=False)

    with gr.Row():
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(height=400, show_copy_button=True, show_share_button=True, 
                               avatar_images=(AIGC_AVATAR_PATH, DATAWHALE_AVATAR_PATH))
            msg = gr.Textbox(label="Prompt/问题")

            with gr.Row():
                qa_btn = gr.Button("Chat with QA")
                clear = gr.ClearButton(components=[chatbot], value="Clear console")

        with gr.Column(scale=1):
            model_argument = gr.Accordion("参数配置", open=False)
            with model_argument:
                temperature = gr.Slider(0, 1, value=0.3, step=0.01, 
                                      label="Temperature", interactive=True)
                top_k = gr.Slider(1, 10, value=4, step=1, 
                                label="Top K", interactive=True)

    # 设置按钮事件 - 关键修改点
    qa_btn.click(
        fn=model_center.answer,
        inputs=[
            msg,  # question
            chatbot,  # chat_history
            gr.State(value=INIT_LLM),  # model (固定值)
            temperature,  # temperature
            top_k  # top_k
        ],
        outputs=[msg, chatbot]
    )
    
    msg.submit(
        fn=respond,
        inputs=[msg, chatbot, temperature],
        outputs=[msg, chatbot]
    )
    
    clear.click(model_center.clear_history)

    gr.Markdown("""提醒：<br>
    1. 使用中如果出现异常，将会在文本输入框进行展示，请不要惊慌。<br>
    2. 点击Clear console可以清除历史记录。<br>
    """)

# 启动应用
demo.launch()