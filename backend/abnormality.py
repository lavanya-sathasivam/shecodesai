import pandas as pd

ranges = pd.read_csv("dataset/reference_ranges.csv")

ranges["low"] = pd.to_numeric(ranges["low"], errors="coerce")
ranges["high"] = pd.to_numeric(ranges["high"], errors="coerce")


def detect_abnormal(values):

    results = []

    for test, value in values.items():

        row = ranges[ranges["name"] == test]

        if row.empty:
            continue

        low = float(row.iloc[0]["low"])
        high = float(row.iloc[0]["high"])

        try:
            value = float(value)
        except:
            continue

        status = "NORMAL"

        if value < low:
            status = "LOW"

        elif value > high:
            status = "HIGH"

        results.append({
            "test": test,
            "value": value,
            "low": low,
            "high": high,
            "status": status
        })

    return results