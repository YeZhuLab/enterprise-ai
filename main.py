from dotenv import load_dotenv #把 .env 文件里的内容加载成环境变量。
from openai import OpenAI
import json
from datetime import datetime


# 读取 .env 文件
load_dotenv() #这样 OpenAI() 就能自动找到你的 API Key。

# 创建 OpenAI 客户端，以后所有请求都会通过这个 client 发出去。
client = OpenAI()


# ===========================
# Tools
# ===========================

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_two_numbers(a, b):
    return "i love myself"

tools = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Get the current local time.",
    },
    {
        "type": "function",
        "name": "add_two_numbers",
        "description": "get the sum of two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "integer",
                    "description": "The first number."
                },
                "b": {
                    "type": "integer",
                    "description": "The second number."
                }
            },
        "required": ["a", "b"]
    }
    }
]

# ===========================
# Conversation History
# ===========================
messages = [
    {
        "role": "system",
        "content": "You are an AI Engineering Mentor. Your goal is to help the user become a professional AI Engineer. Explain concepts step by step. Prefer teaching over directly giving answers. Encourage the user to think before giving solutions. Focus on practical software engineering and AI development skills.Whenever a suitable tool is available, always use the tool instead of answering from your own knowledge."
    }
]

# ===========================
# Chat Loop
# ===========================

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

    # ---------------------------
    # First API Call
    # ---------------------------
    response = client.responses.create(
        model="gpt-5",
        input=messages,
        tools=tools,
    )

    # ---------------------------
    # Find Tool Call
    # ---------------------------
    tool_call = None

    for item in response.output:
        if item.type == "function_call":
            tool_call = item
            break
            
    if tool_call is not None:
        print("=" * 30)
        print("Calling Tool")
        print("Tool:", tool_call.name)
        print("Arguments:", tool_call.arguments)
        print("=" * 30)

    # ---------------------------
    # Second API Call
    # ---------------------------

    if tool_call is not None and tool_call.name == "add_two_numbers":
        args = json.loads(tool_call.arguments)
        result = add_two_numbers(
            args["a"],
            args["b"]
        )
        print("Result:", result)
        response = client.responses.create(
        model="gpt-5",
        previous_response_id=response.id, #这一次 Responses API 的完整上下文。
        input=[
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(result), #transformed into string
            }
        ]
    )

    messages.append({
        "role":"assistant",
        "content": response.output_text
    })

    print("\nGPT:")
    print(response.output_text)

    #print(response.output_text)
    #print(response.id)
    #print("------")
    #print(type(response))
