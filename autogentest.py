llama3 = {
"config_list": [

    {
        #'model': "qwen:14b",
        #'base_url': "http://oneapi.marketineok.com/v1/",
        'model': "qwen2.5:0.5b",
        'base_url': "http://47.104.252.239:13000/v1/",
        'api_key': "sk-96jl4cT87BJcvT806cC7EaB4967d46A89e3f5e792e7020Df"
    },
  ],
  "cache_seed": None,
}


qwen2 = {
"config_list": [
    {
        'model': "qwen2.5:0.5b",
        'base_url': "http://47.104.252.239:13000/v1/",
        'api_key': "sk-96jl4cT87BJcvT806cC7EaB4967d46A89e3f5e792e7020Df"
    },
  ],
  "cache_seed": None,
}


from autogen import ConversableAgent

qwen11 = ConversableAgent(

  "qwen2",

	llm_config=qwen2,

	system_message="你的名字叫qwen，你是一个参考高考学生。你的角色是根据指定主题创作引人入胜且信息丰富的文章，并且根据你的同事llama3的建议来修改和完善你创作的文章，每当你收到llama3的建议时，都要根据llama3的建议给出修改和完善后的完整文章。",

)

llama31 = ConversableAgent(

  "llama3",

	llm_config=llama3,

	system_message="你的名字叫llama3，你的角色是一个高考作文阅卷老师。你的任务是针对你的同事qwen所写的文章评估并提出改进建议，每次对话你都要对文章作出评估并给出修改建议。",
)

chat_result = llama31.initiate_chat(qwen11, message="qwen，随着互联网的普及、人工智能的应用，越来越多的问题能很快得到答案。那么，我们的问题是否会越来越少？以上材料引发了你怎样的联想和思考？请写一篇文章。要求：选准角度，确定立意，明确文体，自拟标题；不要套作，不得抄袭；不得泄露个人信息；不少于800字", max_turns=4)
