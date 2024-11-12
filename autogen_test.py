import autogen

config_list_chatglm = [
    {
        #'model': "qwen:14b",
        #'base_url': "http://oneapi.marketineok.com/v1/",
        #'api_key': "sk-hsYtzf11VBOaiWVf16D596D177F14928908049C08cDb0269"
        'model': "qwen2.5:0.5b",
        'base_url': "http://47.104.252.239:13000/v1/",
        'api_key': "sk-96jl4cT87BJcvT806cC7EaB4967d46A89e3f5e792e7020Df"
    }
]

config_list_qwen = [
    {
        'model': "qwen2.5:0.5b",
        'base_url': "http://47.104.252.239:13000/v1/",
        'api_key': "sk-96jl4cT87BJcvT806cC7EaB4967d46A89e3f5e792e7020Df"
    }
]

llm_config_chatglm={
    "config_list": config_list_chatglm,
}

llm_config_qwen={
    "config_list": config_list_qwen,
}

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_chatglm
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config=False,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    #code_execution_config={"work_dir": "web"},
    llm_config=llm_config_qwen,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task="""
如何让转发/点赞的人发财？！
"""

user_proxy.initiate_chat(coder, message=task)
