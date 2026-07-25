from dotenv import load_dotenv #把 .env 文件里的内容加载成环境变量。
from openai import OpenAI

# 读取 .env 文件
load_dotenv() #这样 OpenAI() 就能自动找到你的 API Key。

# 创建 OpenAI 客户端，以后所有请求都会通过这个 client 发出去。
client = OpenAI()

# 调用 GPT，向 OpenAI 服务器发送请求。
while True:
    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    response = client.responses.create(
        model="gpt-5",
        input=question
    )

    print("\nGPT:")
    print(response.output_text)