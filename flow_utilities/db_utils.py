import pandas as pd

def load_df_to_db(df: pd.DataFrame, table_name: str, schema: str = "jaffle_shop") -> None:
    print('df head: ', df.head(5))