import requests as rq
import pandas as pd
import json


def request_data(url: str, return_df=True):
    response = rq.get(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        },
    )
    if response.status_code == 200:
        return pd.DataFrame(response.json()) if return_df else response.json()
    return pd.DataFrame([])


def read_config(fname: str = "config.json") -> dict:
    with open(fname, "r") as f:
        config = json.loads(f.read())
    return config


def get_sushi_tvl_on_polygon(trunc_date="daily") -> pd.DataFrame:
    urls = read_config()
    url = urls["SUSHI"]["TVL"]
    r = request_data(url=url, return_df=False)
    df = pd.DataFrame(r["chainTvls"]["Polygon"]["tvl"])
    df["Date"] = pd.to_datetime(df["date"], unit="s")
    df["Sushi_TVL"] = df["totalLiquidityUSD"].round(0).astype(int)
    del df["totalLiquidityUSD"]
    df = trunc_by(data=df, by=trunc_date)

    return df


def get_polygon_tvl(trunc_date="daily") -> pd.DataFrame:
    urls = read_config()
    url = urls["POLYGON"]["TVL"]
    r = request_data(url=url, return_df=False)
    df = pd.DataFrame(r)
    df["Date"] = pd.to_datetime(df["date"], unit="s")
    df["Polygon_TVL"] = df["totalLiquidityUSD"].round(0).astype(int)
    del df["totalLiquidityUSD"]
    df = trunc_by(data=df, by=trunc_date)

    return df


def get_all_tvl(trunc_date: str = "daily") -> pd.DataFrame:
    sushi_tvl = get_sushi_tvl_on_polygon(trunc_date=trunc_date)
    polygon_tvl = get_polygon_tvl(trunc_date=trunc_date)
    sushi_tvl["Context"] = "sushi"
    polygon_tvl["Context"] = "polygon"

    return pd.concat(
        [
            sushi_tvl.rename({"Sushi_TVL": "TVL"}, axis=1),
            polygon_tvl.rename({"Polygon_TVL": "TVL"}, axis=1),
        ]
    )


def trunc_by(data: pd.DataFrame, by: str = "W-MON") -> pd.DataFrame:
    if by == "daily":
        return data[:-1]
    if by == "monthly":
        by_change = "MS"
    elif by == "weekly":
        by_change = "W-MON"
    return (
        data.resample(by_change, label="left", closed="left", on="Date")
        .sum()
        .reset_index()
        .sort_values(by="Date")
    )


def get_date_truncations(self, data: pd.DataFrame) -> dict:
    """
    Creates Weekly and Monthly  dict.

    Args:
        data (pd.DataFrame): Dataframe of Daily data.

    Returns:
            dict: Daily, Weekly and Monthly  dataframes.
    """
    weekly = trunc_by(data=data, by="W")
    monthly = trunc_by(data=data, by="M")
    return {"daily": data, "weekly": weekly, "monthly": monthly}


def anchor_stats(trunc_date: str) -> pd.DataFrame:
    urls = [
        "https://api.flipsidecrypto.com/api/v2/queries/0340f54a-b4dc-4797-b9ce-f26ce35b2f64/data/latest",  # Deposit estimate
        "https://api.flipsidecrypto.com/api/v2/queries/a8f67d65-7066-4fb4-8210-bb5bea10599a/data/latest",  # Borrow estimate
    ]

    deposit_daily = request_data(url=urls[0], return_df=True)
    withdraw_daily = request_data(url=urls[1], return_df=True)
    deposit_daily["DATE"] = pd.to_datetime(deposit_daily["DATE"])
    withdraw_daily["DATE"] = pd.to_datetime(withdraw_daily["DATE"])
    if trunc_date == "daily":
        return (deposit_daily, withdraw_daily)
    elif trunc_date == "weekly":
        return (trunc_by(deposit_daily, by="W"), trunc_by(withdraw_daily, by="W"))
    else:
        return (trunc_by(deposit_daily, by="M"), trunc_by(withdraw_daily, by="M"))


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
