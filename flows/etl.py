from flow_utilities.db_utils import load_df_to_db
from flow_utilities.prefect_configs import set_run_config, set_storage
import pandas as pd
import prefect
from prefect import task, Flow
from prefect.executors import LocalDaskExecutor
from prefect.engine.results import PrefectResult
from datetime import datetime
import time
import json

FLOW_NAME = "etl"

@task(result=PrefectResult())
def extract_and_load(dataset: str) -> None:
    logger = prefect.context.get("logger")
    logger.info(f"Started at: {datetime.now()}")
    time.sleep(10)
    file = f"https://raw.githubusercontent.com/anna-geller/jaffle_shop/main/data/{dataset}.csv"
    df = pd.read_csv(file)
    load_df_to_db(df, dataset)
    logger.info("Dataset %s with %d rows loaded to DB", dataset, len(df))
    logger.info(f"Ended at: {datetime.now()}")
    return json.dumps({f"length of dataset {dataset}": len(df)})


with Flow(
    FLOW_NAME,
    executor=LocalDaskExecutor(),
    storage=set_storage(FLOW_NAME),
    run_config=set_run_config(),
) as flow:
    datasets = ["raw_customers", "raw_orders", "raw_payments"]
    dataframes = extract_and_load.map(datasets)