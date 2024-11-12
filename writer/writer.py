#
# 使用AutoGen编写一个多角色的具有反思能力的写手Agent
#
import autogen
from autogen import agentchat
from llm_config_local import ConfigManager


def reflection_message(recipient, message, sender, config):
    return f"""Review the following content. 
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"""


config_man = ConfigManager()
llm_config = config_man.get_llm_config()

task = '''
        编写一个小红书爆款文案，根据AI对当前社会的影响来编写，大概100字左右.
       '''

writer = agentchat.AssistantAgent(
    name="Writer",
    system_message="You are a writer. You write engaging and concise "
                   "blogpost (with title) on given topics. You must polish your "
                   "writing based on the feedback you receive and give a refined "
                   "version. Only return your final work without additional comments. Write in chinese.",
    llm_config=llm_config,
)

critic = autogen.AssistantAgent(
    name="Critic",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    system_message="You are a critic. You review the work of "
                   "the writer and provide constructive "
                   "feedback to help improve the quality of the content.",
)

# 负责优化内容以提高其在搜索引擎中的排名，吸引流量。我们通过设置系统消息来实现这一点，下同。
SEO_reviewer = autogen.AssistantAgent(
    name="SEO Reviewer",
    llm_config=llm_config,
    system_message="You are an SEO reviewer, known for "
                   "your ability to optimize content for search engines, "
                   "ensuring that it ranks well and attracts organic traffic. "
                   "Make sure your suggestion is concise (within 3 bullet points), "
                   "concrete and to the point. "
                   "Begin the review by stating your role. Write in chinese.",
)

# 确保内容合法合规。
legal_reviewer = autogen.AssistantAgent(
    name="Legal Reviewer",
    llm_config=llm_config,
    system_message="You are a legal reviewer, known for "
                   "your ability to ensure that content is legally compliant "
                   "and free from any potential legal issues. "
                   "Make sure your suggestion is concise (within 3 bullet points), "
                   "concrete and to the point. "
                   "Begin the review by stating your role. Write in chinese.",
)

# 确保内容符合伦理规范，没有潜在的伦理问题。
ethics_reviewer = autogen.AssistantAgent(
    name="Ethics Reviewer",
    llm_config=llm_config,
    system_message="You are an ethics reviewer, known for "
                   "your ability to ensure that content is ethically sound "
                   "and free from any potential ethical issues. "
                   "Make sure your suggestion is concise (within 3 bullet points), "
                   "concrete and to the point. "
                   "Begin the review by stating your role.  Write in chinese.",
)

# 汇总所有评论代理的意见，给出最终建议。
meta_reviewer = autogen.AssistantAgent(
    name="Meta Reviewer",
    llm_config=llm_config,
    system_message="You are a meta reviewer, you aggragate and review "
                   "the work of other reviewers and give a final suggestion on the content. Write in chinese.",
)

review_chats = [
    {
        "recipient": SEO_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return review into as JSON object only:"
                              "{'Reviewer': '', 'Review': ''}. Here Reviewer should be your role",
        },
        "max_turns": 1,
    },
    {
        "recipient": legal_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return review into as JSON object only:"
                              "{'Reviewer': '', 'Review': ''}.",
        },
        "max_turns": 1,
    },
    {
        "recipient": ethics_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": "Return review into as JSON object only:"
                              "{'reviewer': '', 'review': ''}",
        },
        "max_turns": 1,
    },
    {
        "recipient": meta_reviewer,
        "message": "Aggregrate feedback from all reviewers and give final suggestions on the writing.",
        "max_turns": 1,
    },
]

critic.register_nested_chats(
    review_chats,
    trigger=writer,
)

res = critic.initiate_chat(
    recipient=writer,
    message=task,
    max_turns=2,
    summary_method="last_msg"
)

print(res.summary)



