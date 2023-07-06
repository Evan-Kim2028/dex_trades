import asyncio
import itertools
import json
import os

from dataclasses import dataclass
from queryportal.subgraphinterface import SubgraphInterface
from datetime import datetime, timedelta

import polars as pl
pl.Config.set_fmt_str_lengths(200)


@dataclass
class DexTrades:
    """
    Main class that users interact through
    """
    sgi = None

    def __post_init__(self):
        self.sgi = self.load_endpoints()

    def load_endpoints(self) -> SubgraphInterface:
        """
        Load endpoints from subgraphs.csv file when class is initialized
        """
        
        # load subgraphs.csv file
        subgraphs = pl.read_csv('src/subgraphs.csv')

        # take protocol and endpoint and create a new dictionary
        subgraph_dict = dict(zip(subgraphs['protocol'], subgraphs['endpoint']))

        return SubgraphInterface(endpoints=subgraph_dict)

    def make_data_folders(self):
        # make a folder called data
        if not os.path.exists('data'):
            os.makedirs('data')

        for subgraph in list(self.sgi.subject.subgraphs.keys()):
            os.makedirs(f'data/{subgraph}', exist_ok=True)

    def query_trades(self, start_date: str, date_range: int, query_size: int = 1500):
        # initial params might be query_paths, query_size, and a filter?

        self.make_data_folders()

        # convert start date from str to datetime
        format_string = "%Y-%m-%d"
        datetime_obj = datetime.strptime(start_date, format_string)


        # Fields to be returned from the query
        query_paths = [
            'hash',
            'to',
            'from',
            'blockNumber',
            'timestamp',
            'tokenIn_symbol',
            'tokenOut_symbol',
            'amountIn',
            'amountOut',
            'amountInUSD',
            'amountOutUSD',
            'pool_id',
            'pool_name'
        ]

        def process_subgraph(subgraph, start_date, end_date):
            """
            Function to be called asynchronously
            """

            filter = {
                'timestamp_gte': int(start_date.timestamp()),
                'timestamp_lte': int(end_date.timestamp()),
            }

            # NEW - trying new way of saving the file
            self.sgi.query_entity(
                query_size=query_size,
                entity='swaps',
                name=subgraph,
                query_paths=query_paths,
                filter_dict=filter,
                orderBy='timestamp',
                saved_file_name=f'data/{subgraph}/{subgraph}_swaps_{start_date.strftime("%m-%d")}_{end_date.strftime("%m-%d")}'
                )
                

        async def main():
            subgraph_keys = list(self.sgi.subject.subgraphs.keys())
            date_ranges = [(start_date, start_date + timedelta(days=1)) for start_date in [datetime_obj + timedelta(days=i) for i in range(0, date_range, 1)]]

            await asyncio.gather(*[asyncio.to_thread(process_subgraph, subgraph, start_date, end_date) for subgraph, (start_date, end_date) in itertools.product(subgraph_keys, date_ranges)])


        # Run the asyncio event loop
        asyncio.run(main())    

        # save to file
