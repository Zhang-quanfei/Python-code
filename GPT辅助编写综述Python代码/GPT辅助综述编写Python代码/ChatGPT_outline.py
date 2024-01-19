import openai
import pandas as pd
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


topic_1 = '数字金融'
topic_2 = '企业创新'
df = pd.read_csv(f"./{topic_1}+{topic_2}/筛选结果.csv")
result = ''
for i, j, z ,x,y in zip(df["作者"], df["所属期数"], df["文献来源"], df['篇名'],df["摘要"]):
    result += f"'{i}','{j}','{z}','{x}','{y}'\n"

prompt = f"""
作为一位『“{topic_1}”和“{topic_2}”』领域的专家，您了解该领域所有的前沿知识、专业名词、模型方法、\
算法技术等必备的知识，同时具有较好的文献阅读能力和信息总结能力。

我即将以csv文件的格式给您发送论文信息。第一列是作者，第二列是年（期），第三列是刊名，第四列是文献题名\
第五列是文章的摘要。

现在，我希望根据这些文献的信息，写一篇专业性较强的综述文章。请你从专业的角度出发，为我的综述拟一份大纲。\
要求大纲的格式标准，涵盖一篇标准综述应该拥有的内容。并且注明各个部分需要参考的所有文献，标注的方式为：（参考文献：作者，篇名）

最后，为这篇综述文章取一个合适的标题。

论文信息：
```
{result}
```
"""

print('prompt导入成功！')
response = get_completion(prompt)
print(response)
with open(f"./{topic_1}+{topic_2}/大纲.md","w",encoding="utf-8") as file:
    file.write(response)
print(f"文献内容整理成功！共用时{time.time()-start_time}")