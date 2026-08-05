from dotenv import load_dotenv #把 .env 文件里的内容加载成环境变量。
from openai import OpenAI
import json
from datetime import datetime
from search_code import search_code


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
    return a + b

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
    },
    {
        "type": "function",
        "name": "search_code",
        "description": "Search the Python codebase for code related to the user's query and return relevant code snippets.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                     "type": "string",
                     "description": "The function name, variable name, or code-related keyword to search for."
                }
            },
            "required": ["query"]
        }
    }
]

#get_current_time表示：函数对象（Function Object）而：get_current_time()表示：立即执行函数。

tool_map = {
    "get_current_time": get_current_time,
    "add_two_numbers": add_two_numbers,
    "search_code": search_code,
}


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
    first_response = client.responses.create(
        model="gpt-5",
        input=messages,
        tools=tools,
    )


    # ---------------------------
    # Find Tool Call
    # ---------------------------
    tool_calls = []

    for item in first_response.output:
        if item.type == "function_call":
            tool_calls.append(item)
            
    if tool_calls:
        print("=" * 30)
        print(f"Calling {len(tool_calls)} tool(s)")
        print("=" * 30)

    # ---------------------------
    # Second API Call
    # ---------------------------
    
    tool_outputs = []
    for tool_call in tool_calls:
        tool_func = tool_map[tool_call.name]
        tool_args = json.loads(tool_call.arguments)
        result = tool_func(**tool_args)
        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(result),
            }
        )
    
    if tool_calls:
        second_response = client.responses.create(
            model="gpt-5",
            previous_response_id=first_response.id, #这一次 Responses API 的完整上下文。
            input=tool_outputs
        )
    else:
        second_response = first_response
        
    messages.append({
        "role":"assistant",
        "content": second_response.output_text
    })

    print("\nGPT:")
    print(second_response.output_text)

    #print(response.output_text)
    #print(response.id)
    #print("------")
    #print(type(response))
