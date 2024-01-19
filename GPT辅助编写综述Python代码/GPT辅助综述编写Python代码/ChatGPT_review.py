import openai
import time
import pandas as pd


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
with open(f'./{topic_1}+{topic_2}/大纲.md', 'r',encoding="utf-8") as file:
    outline = file.readlines()

df = pd.read_csv(f"./{topic_1}+{topic_2}/筛选结果.csv")
result = ''
for i, j, z ,x,y in zip(df["作者"], df["所属期数"], df["文献来源"], df['篇名'],df["摘要"]):
    result += f"'{i}','{j}','{z}','{x}','{y}'\n"


prompt = f"""
作为一位『“{topic_1}”和“{topic_2}”』领域的专家，您了解该领域所有的前沿知识、专业名词、模型方法、\
算法技术等必备的知识，同时具有较好的文献阅读能力和信息总结能力。

我即将以csv文件的格式给您发送论文信息。第一列是作者，第二列是年（期），第三列是刊名，第四列是文献题名\
第五列是文章的摘要。

同时，我会给你发送一份综述的大纲，请你据此写一篇专业性强的综述。大纲中提到的参考文献都可以在论文信息中找到，\
请你根据大纲找到对应的参考文献，从中提取出综述需要的内容进行编写。要求在文中引用参考文章的观点或者结论时，需要在这个句\
子后面用（作者，年份）标注出来。同时，正文部分不能仅仅罗列其他文章的观点或结论，还需要你自己思考这个结论的意义，并做出\
评价，用经济学的原理和方法去解释这一结论或者观点。正文部分不少于2000字。

综述以markdown的格式展示。

综述大纲：
```
{outline}
```

论文信息：
```
{result}
```
"""

print('prompt导入成功！')
response = get_completion(prompt)
print(response)
with open(f"./{topic_1}+{topic_2}/综述.md","w",encoding="utf-8") as file:
    file.write(response)
print(f"综述保存成功！共用时{time.time()-start_time}")