import pandas.io.sql as sql
from research.lhb_db_connection import get_db_connection

# 获取连接
con = get_db_connection()

# 获取汇总表中所有数据
df = sql.read_sql("select * from lhb_detail_dfcf",  con)

# 根据原因进行分组，每个原因列示总共记录条数，最早上榜记录，最晚上榜记录
yyb_group = df['lhb_date'].groupby(df['yyb_name'])
reason_df = yyb_group.agg([('total', 'nunique'), ('first_date', 'min'), ('last_date', 'max')])
reason_df = reason_df.sort_values('total', ascending=False)
reason_df.to_csv('data/yyb_group.csv')

