import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import argparse
import os
from tqdm import tqdm

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db

    # Ingest Parquet file
    file_name = 'data.parquet'
    url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet'
    os.system(f'wget {url} -O {file_name}')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    pf = pq.ParquetFile(file_name)
    batch_size = 10000
    
    for data in tqdm(pf.iter_batches(batch_size=batch_size), total=pf.metadata.num_rows // batch_size):
        df = data.to_pandas()
        df.to_sql(name='yellow_taxi_trips', con=engine, if_exists='append')
    
    # Ingest CSV file
    file_name = 'zones.csv'
    url = 'https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'
    os.system(f'wget {url} -O {file_name}')
    
    df_zones = pd.read_csv(file_name)
    df_zones.to_sql(name='zones', con=engine, if_exists='replace')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest data to Postgres")
    parser.add_argument('--user', help="user name for postgres")
    parser.add_argument('--password', help="password for postgres")
    parser.add_argument('--host', help="host for postgres")
    parser.add_argument('--port', help="port for postgres")
    parser.add_argument('--db', help="database name for postgres")
    
    args = parser.parse_args()
    main(args)