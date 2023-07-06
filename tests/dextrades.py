from dex_trades import DexTrades
from preprocess_dex import *


dex_trades = DexTrades()


# query subgraphs
dex_trades.query_trades(start_date='2021-07-01', date_range=5, query_size = 750)

# combine daily dfs into a single df
for dex in ['balancerv2', 'curve', 'uniswapv3']:
    combine_dfs(f'data/{dex}', dex)