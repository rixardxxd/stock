import pandas.io.sql as sql
from research.lhb_db_connection import get_db_connection


# 日期聚合函数，用于将特定股票的所有上榜日期汇总成列表
def date_aggregate(arr):
    arr_str = arr.map(lambda x: x.strftime("%Y-%m-%d"))
    return ",".join(arr_str.values)


# 获取连接
con = get_db_connection()

# 获取汇总表中所有数据,去掉重复的上榜数据
df = sql.read_sql("select lhb_date,stock_id from lhb_detail_dfcf where yyb_name not like '%机构专用%'", con)
df = df[['lhb_date', 'stock_id']]
df = df.drop_duplicates(subset=['lhb_date', 'stock_id'], keep='first')
stock_group = df['lhb_date'].groupby(df['stock_id'])
stock_df = stock_group.agg([('date_list', date_aggregate)])
# 写入本地文件，写CSV文件时，股票代码总是被当作数字
# 所以深市个股总是被省略前缀0，这里添加交易所后缀来强制转化为字符串
pattern = lambda x : x + '.SH' if x[0] == '6' else x + '.SZ'
stock_df.index = stock_df.index.map(pattern)
stock_df.to_csv('data/yyb_non_institution_group.csv')
