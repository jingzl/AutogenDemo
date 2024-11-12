import json


class ConfigManager:
    def __init__(self):
        # 这里需要修改你的LLM平台的url
        self.base_url = 'http://47.104.252.239:13000/v1/'

    def get_llm_config(self):
        llm_config = {
            "model": "qwen2.5:0.5b",
            "base_url": self.base_url,
            "api_key": "sk-96jl4cT87BJcvT806cC7EaB4967d46A89e3f5e792e7020Df",
            "price": [1, 10],
        }
        return llm_config

    def get_config_list(self):
        config_list = [
            {
                "model": "llama3.1:8b",
                "base_url": self.base_url,
                "api_key": "ollama",
                "price": [1, 10],
            },
        ]
        return config_list

