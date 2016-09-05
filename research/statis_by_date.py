import pandas.io.sql as sql
from research.lhb_db_connection import get_db_connection

# 获取连接
con = get_db_connection()

# 获取汇总表中所有数据
df = sql.read_sql("select * from lhb_summary_dfcf",  con)

# 对于同一天内个股多次上榜的记录进行去重
df = df.drop_duplicates(['lhb_date','stock_id'])

# 根据日期进行分组
date_group = df['lhb_date'].groupby(df['lhb_date'])
date_group.count().to_csv('data/date_group.csv')

