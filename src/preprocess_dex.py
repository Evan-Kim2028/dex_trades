import polars as pl
import os

pl.Config.set_fmt_str_lengths(200)


def combine_dfs(folder: str, filename: str):
    """
    Combines all daily dfs in a folder into a single df
    """
    dfs_agg = []

    for file in os.listdir(folder):
        daily_df = pl.read_parquet(f'{folder}/{file}')
        dfs_agg.append(daily_df)


    # concat all daily_dfs
    combined_df = pl.concat(dfs_agg)


    # convert timestamp to datetime
    combined_df = combined_df.with_columns(
        pl.from_epoch("timestamp")
    )
    
    # save combined_df to dex_swaps folder
    combined_df.write_parquet(f'data/{filename}_trades.parquet')