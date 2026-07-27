from dotenv import load_dotenv #把 .env 文件里的内容加载成环境变量。
from openai import OpenAI

# 读取 .env 文件
load_dotenv() #这样 OpenAI() 就能自动找到你的 API Key。

# 创建 OpenAI 客户端，以后所有请求都会通过这个 client 发出去。
client = OpenAI()

messages = [
    {
        "role": "system",
        "content": "You are an AI Engineering Mentor. Your goal is to help the user become a professional AI Engineer. Explain concepts step by step. Prefer teaching over directly giving answers. Encourage the user to think before giving solutions. Focus on practical software engineering and AI development skills."
    }
]


# 调用 GPT，向 OpenAI 服务器发送请求。
while True:
    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    messages.append(
    {
        "role": "user",
        "content": question
    }
)

    response = client.responses.create(
        model="gpt-5",
        input=messages
    )

    messages.append({
        "role":"assistant",
        "content": response.output_text
    })


    print("\nGPT:")
    print(response.output_text)
    #print(response.id)
    #print("------")
    #print(type(response))
