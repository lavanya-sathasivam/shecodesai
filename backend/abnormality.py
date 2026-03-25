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

        # Use the first matching range (in case of duplicates)
        low = float(row.iloc[0]["low"])
        high = float(row.iloc[0]["high"])

        try:
            value = float(value)
        except:
            continue

        # Calculate deviation percentage
        if value < low:
            deviation = (low - value) / low * 100
            if deviation > 30:  # More than 30% below normal
                status = "CRITICAL"
            elif deviation > 15:  # 15-30% below normal
                status = "HIGH"
            else:
                status = "SLIGHTLY_ABNORMAL"
        elif value > high:
            deviation = (value - high) / high * 100
            if deviation > 30:  # More than 30% above normal
                status = "CRITICAL"
            elif deviation > 15:  # 15-30% above normal
                status = "HIGH"
            else:
                status = "SLIGHTLY_ABNORMAL"
        else:
            status = "NORMAL"

        results.append({
            "test": test,
            "value": value,
            "low": low,
            "high": high,
            "status": status
        })

    return results