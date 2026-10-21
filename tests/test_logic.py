"""Offline tests for revenue.py plus a full (networked) execution of the notebook."""
import sys
from pathlib import Path

import nbformat
import pandas as pd
import pytest
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from revenue import common_range, parse_revenue_table  # noqa: E402

HTML = """<html><body>
<table><thead><tr><th>Tesla Annual Revenue (Millions of US $)</th><th>x</th></tr></thead>
<tbody><tr><td>2020</td><td>$31,536</td></tr></tbody></table>
<table><thead><tr><th>Tesla Quarterly Revenue (Millions of US $)</th><th>x</th></tr></thead>
<tbody><tr><td>2021-03-31</td><td>$10,389</td></tr><tr><td>2009-09-30</td><td>$46</td></tr>
<tr><td>2009-06-30</td><td></td></tr><tr><td>2020-12-31</td><td>$10,744</td></tr></tbody></table>
</body></html>"""


def test_revenue_is_numeric_sorted_and_cleaned():
    df = parse_revenue_table(HTML)
    assert df["Revenue"].dtype.kind == "f" and str(df["Date"].dtype).startswith("datetime64")
    assert list(df["Revenue"]) == [46.0, 10744.0, 10389.0]          # sorted by date, empty row dropped
    assert df["Revenue"].max() == 10744.0                           # numeric order, not string order


def test_table_found_by_header_not_position():
    with pytest.raises(ValueError):
        parse_revenue_table(HTML, match="Does Not Exist")


def test_common_range_handles_tz_aware_prices():
    stock = pd.DataFrame({"Date": pd.date_range("2010-06-29", "2026-10-16", freq="D", tz="America/New_York")})
    rev = pd.DataFrame({"Date": pd.to_datetime(["2009-06-30", "2021-03-31"]), "Revenue": [1.0, 2.0]})
    start, end = common_range(stock, rev)
    assert start == pd.Timestamp("2010-06-29") and end == pd.Timestamp("2021-03-31")


def test_notebook_executes_and_plots_numeric_revenue():
    nb = nbformat.read(ROOT / "Tesla_Gme_revenue.ipynb", as_version=4)
    nb.cells.append(nbformat.v4.new_code_cell(
        "assert tesla_revenue.Revenue.dtype.kind == 'f' and gme_revenue.Revenue.dtype.kind == 'f'\n"
        "f = make_graph(tesla_data, tesla_revenue, 'Tesla')\n"
        "assert f.layout.yaxis2.autorange is None\n"
        "assert max(f.data[1].y) == tesla_revenue.Revenue.max()"))
    NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(ROOT)}}).execute()
