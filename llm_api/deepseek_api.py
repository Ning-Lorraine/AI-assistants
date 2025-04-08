# import os
# from dotenv import load_dotenv,find_dotenv
# from openai import OpenAI
# from langchain_openai import ChatOpenAI


# def get_completion_deepseek(model:str,prompt:str,temperature:float=1.0):
#     '''
#     使用DeepSeek API生成文本
#     model: 模型名称
#     messages: 对话历史
#     temperature: 温度
#     '''
#     client = OpenAI(api_key=parse_api_key(model), base_url="https://api.deepseek.com")
#     messages = [
#         {"role": "user", "content": prompt},
#     ]
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         stream=False,
#         temperature=temperature,
#     )
#     # print(response.choices[0].message.content)  
#     return response.choices[0].message.content


# # 从环境变量.env中读取API Key
# def parse_api_key(model:str):
#     load_dotenv(find_dotenv())
#     if model == "deepseek-chat":
#         return os.getenv("DEEPSEEK_API_KEY")
#     else:
#         raise ValueError(f"Model {model} not supported")


# # get_completion_deepseek("deepseek-chat","请分析下面的报错信息,并给出解决措施：pydantic_core_schema__` then you likely need to call `handler.generate_schema(<some type>)` since we do not call `__get_pydantic_core_schema__` on `<some type>` otherwise to avoid infinite recursion. For further information visit https://errors.pydantic.dev/2.10/u/schema-for-unknown-type During handling of the above exception, another exception occurred: Traceback (most recent call last): File /Users/ning/miniconda3/envs/langrag/lib/python3.12/site-packages/uvicorn/protocols/http/h11_impl.py, line 403, in run_asgi result = await app(  # type: ignore[func-returns-value]^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^File '/Users/ning/miniconda3/envs/langrag/lib/python3.12/site-packages/uvicorn/middleware/proxy_headers.py', line 60, in __call__^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^File '/Users/ning/miniconda3/envs/langrag/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py', line 886, in _generate_schema_innerreturn self.match_type(obj)File '/Users/ning/miniconda3/envs/langrag/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py', line 515, in _unknown_type_schemaraise PydanticSchemaGenerationError(pydantic.errors.PydanticSchemaGenerationError: Unable to generate pydantic-core schema for <class 'starlette.requests.Request'>. Set `arbitrary_types_allowed=True` in the model_config to ignore this error or implement `__get_pydantic_core_schema__` on your type to fully support it. If you got this error by calling handler(<some type>) within `__get_pydantic_core_schema__` then you likely need to call `handler.generate_schema(<some type>)` since we do not call `__get_pydantic_core_schema__` on `<some type>` otherwise to avoid infinite recursion.For further information visit https://errors.pydantic.dev/2.10/u/schema-for-unknown-type")
# # get_completion_deepseek("deepseek-chat","你好")

import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from openai import OpenAIError

def get_completion_deepseek(model: str, prompt: str, temperature: float = 1.0):
    '''
    使用DeepSeek API生成文本
    model: 模型名称
    messages: 对话历史
    temperature: 温度
    '''
    try:
        client = OpenAI(api_key=parse_api_key(model), base_url="https://api.deepseek.com")
        messages = [
            {"role": "user", "content": prompt},
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        print(f"OpenAI API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

# 从环境变量.env中读取API Key
def parse_api_key(model: str):
    load_dotenv(find_dotenv())
    if model == "deepseek-chat":
        return os.getenv("DEEPSEEK_API_KEY")
    else:
        raise ValueError(f"Model {model} not supported")

result = get_completion_deepseek("deepseek-chat", "你好")
if result:
    print(result)