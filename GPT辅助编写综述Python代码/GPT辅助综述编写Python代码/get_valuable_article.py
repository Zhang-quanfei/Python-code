import os
import pandas as pd
from datetime import datetime, timedelta

# 1. 读取CSV文件
topic1 = "数字金融"
topic2 = "企业创新"
folder_path = f'./{topic1}+{topic2}/'
csv_file = os.path.join(folder_path, 'result.csv')
df = pd.read_csv(csv_file)

# 2. 格式化日期列
df['发表时间'] = pd.to_datetime(df['发表时间'])

# 3. 添加新列 '年份'，并按照发表年份分组
df['年份'] = df['发表时间'].dt.year
grouped = df.groupby('年份')

# 4. 处理每个年份分组的文章
result = pd.DataFrame()
for year, group in grouped:
    # (1) 计算综合指标
    group['综合指标'] = 0.7 * group['下载频次'] + 0.3 * group['被引频次']

    # (2) 最近三个月内的文章加分
    three_months_ago = datetime.now() - timedelta(days=90)
    group.loc[group['发表时间'] >= three_months_ago, '附加分'] = 100
    group['附加分'].fillna(0, inplace=True)

    # (3) 计算评分并排序
    group['评分'] = group['综合指标'] + group['附加分']
    group.sort_values(by='评分', ascending=False, inplace=True)

    # (4) 选择排名前5%的文章
    num_articles = max(int(len(group) * 0.1), 1)
    selected_articles = group.head(num_articles)
    result = pd.concat([result, selected_articles])

    # 打印每个年份选择的文章数量
    print(f'年份：{year}，选择的文章数量：{len(selected_articles)}')

# 打印总的文章数量
print(f'总的文章数量：{len(result)}')

# 5. 将结果保存到新的CSV文件中
output_file = os.path.join(folder_path, '筛选结果.csv')
result.to_csv(output_file, index=False)
