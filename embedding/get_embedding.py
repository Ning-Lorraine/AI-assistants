# import requests
# import os
# from dotenv import load_dotenv

# # 获取embedding模型

# def get_embedding(text: str) -> dict:
#     """
#     Get embedding for the input text using BAAI/bge-large-zh-v1.5 model.
    
#     Args:
#         text (str): The text to be converted to embedding
        
#     Returns:
#         dict: The response from the embedding API
#     """
#     # Load environment variables
#     load_dotenv()
    
#     url = "https://api.siliconflow.cn/v1/embeddings"
    
#     payload = {
#         "model": "BAAI/bge-large-zh-v1.5",
#         "input": text,
#         "encoding_format": "float"
#     }
    
#     headers = {
#         "Authorization": f"Bearer {os.getenv('BAAI_API_KEY')}",
#         "Content-Type": "application/json"
#     }
    
#     response = requests.request("POST", url, json=payload, headers=headers)
#     return response.json()

# # if __name__ == "__main__":
# #     # Example usage
# #     test_text = "Silicon flow embedding online: fast, affordable, and high-quality embedding services. come try it out!"
# #     result = get_embedding(test_text)
# #     print(result)


from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional
import requests
from dotenv import load_dotenv

from langchain_core.embeddings import Embeddings
from pydantic import BaseModel, root_validator
from langchain_core.utils import get_from_dict_or_env

logger = logging.getLogger(__name__)

class BAAIEmbeddings(BaseModel, Embeddings):
    """BAAI Embeddings embedding models."""

    baai_api_key: Optional[str] = None
    """BAAI application apikey"""
    
    model_name: str = "BAAI/bge-large-zh-v1.5"
    """Model name to use"""
    
    url: str = "https://api.siliconflow.cn/v1/embeddings"
    """API endpoint URL"""

    @root_validator(skip_on_failure=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        values["baai_api_key"] = get_from_dict_or_env(
            values,
            "baai_api_key",
            "BAAI_API_KEY",
        )
        return values

    def _embed(self, text: str) -> List[float]:
        """Get embedding for a single text."""
        headers = {
            "Authorization": f"Bearer {self.baai_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_name,
            "input": text,
            "encoding_format": "float"
        }
        
        try:
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result["data"][0]["embedding"]
        except Exception as e:
            raise ValueError(f"Error raised by BAAI embedding API: {e}")

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single text.
        
        Args:
            text (str): The text to embed.
            
        Returns:
            List[float]: The embedding vector.
        """
        return self._embed(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of texts.
        
        Args:
            texts (List[str]): The list of texts to embed.
            
        Returns:
            List[List[float]]: List of embedding vectors.
        """
        return [self._embed(text) for text in texts]

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Asynchronous Embed search docs."""
        raise NotImplementedError(
            "BAAI embedding API does not support asynchronous requests")

    async def aembed_query(self, text: str) -> List[float]:
        """Asynchronous Embed query text."""
        raise NotImplementedError(
            "BAAI embedding API does not support asynchronous requests")