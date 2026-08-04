def search_code(query):
    import os

    files = os.listdir(".") #遍历文件
   # query = "get_current_time"

    for file in files:
        if file.endswith(".py"):
            with open(file, "r") as f: #文件读取
                lines = f.readlines()
            for index, line in enumerate(lines):
                if query in line:
                    context = lines[index-5:index+6]
                    return "".join(context)
    return "No matching code found."
