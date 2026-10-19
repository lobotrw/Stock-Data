"""Helpers for Tesla_Gme_revenue.ipynb: parse the revenue tables and align date ranges."""
from __future__ import annotations

import pandas as pd
from bs4 import BeautifulSoup


def parse_revenue_table(html: bytes | str, match: str = "Quarterly Revenue") -> pd.DataFrame:
    """Find the table whose header contains ``match`` (not a fixed tbody position) and return
    Date (datetime64) and Revenue (float, $US millions), sorted by date, empty rows dropped."""
    soup = BeautifulSoup(html, "html.parser")
    table = next((t for t in soup.find_all("table")
                  if t.find("th") and match.lower() in t.find("th").get_text().lower()), None)
    if table is None:
        raise ValueError(f"No table with a header containing {match!r}")
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        td = tr.find_all("td")
        if len(td) >= 2:
            rows.append({"Date": td[0].get_text(strip=True), "Revenue": td[1].get_text(strip=True)})
    df = pd.DataFrame(rows)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Revenue"] = pd.to_numeric(df["Revenue"].str.replace(r"[$,]", "", regex=True), errors="coerce")
    df = df.dropna().sort_values("Date").reset_index(drop=True)
    df["Revenue"] = df["Revenue"].astype(float)
    return df


def common_range(stock: pd.DataFrame, revenue: pd.DataFrame):
    """Date window covered by both series: [max of starts, min of ends] as tz-naive Timestamps."""
    s = pd.to_datetime(stock["Date"]).dt.tz_localize(None) if getattr(stock["Date"].dt, "tz", None) else pd.to_datetime(stock["Date"])
    start = max(s.min(), revenue["Date"].min())
    end = min(s.max(), revenue["Date"].max())
    return start, end
