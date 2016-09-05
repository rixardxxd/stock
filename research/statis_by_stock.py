import pandas as pd
import pandas.io.sql as sql
from research.lhb_db_connection import get_db_connection


# 日期聚合函数，用于将特定股票的所有上榜日期汇总成列表
def date_aggregate(arr):
    arr_str = arr.map(lambda x : x.strftime("%Y-%m-%d"))
    return ",".join(arr_str.values)

# 获取汇总表中所有数据
con = get_db_connection()

# 获取汇总表中所有数据
df = sql.read_sql("select * from lhb_summary_dfcf",  con)

# 对于同一天内个股多次上榜的记录进行去重
df = df.drop_duplicates(['lhb_date','stock_id'])

# 根据stock_id进行分组，并按日期聚合
stock_group = df['lhb_date'].groupby(df['stock_id'])
stock_df = stock_group.agg([('date_list', date_aggregate)])

# 写入本地文件，写CSV文件时，股票代码总是被当作数字
# 所以深市个股总是被省略前缀0，这里添加交易所后缀来强制转化为字符串
pattern = lambda x : x + '.SH' if x[0] == '6' else x + '.SZ'
stock_df.index = stock_df.index.map(pattern)
stock_df.to_csv('data/stock_group.csv')


# tmp = pd.read_csv(r'D:\workspace\stock\research\data\stock_group.csv')
# for item in tmp['date_list'].values:
#     date_list = item.split(',')
#     print(len(date_list))
#     for date in date_list:
#         print(date)