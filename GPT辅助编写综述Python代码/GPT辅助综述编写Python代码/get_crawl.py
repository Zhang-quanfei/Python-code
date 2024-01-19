import openai
import time

start_time = time.time()

with open('sk_token.txt', 'r', encoding='utf-8')as file:
    openai.api_key = file.read().strip()


def get_completion(prompt, model="gpt-3.5-turbo-16k"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # 此参数为控制答案的随机程度，为0一般总是会得到相同的答案
    )
    return response.choices[0].message["content"]

# 读取cURL文件内容
with open('cURL.txt', 'r',encoding="utf-8") as file:
    curl_commands = file.readlines()

prompt = f"""
作为一个专业的Python爬虫工程师，请你将下面这段由三个反引号界定的cURL改写为一段严谨而可行的Python爬虫代码。
只需要输出完整的代码即可，代码不需要用代码块的格式，不要输出其他东西。
```
{curl_commands}
```
"""


response = get_completion(prompt)

# 将生成的Python爬虫代码写入文件
with open('crawl.py', 'w',encoding='utf-8') as file2:
    file2.write(response)

print(f"转换完成，已生成crawl.py文件。共用时{time.time()-start_time}")
