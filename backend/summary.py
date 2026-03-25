def generate_summary(results):

    summary = []

    for r in results:

        test = r["test"]
        status = r["status"]
        value = r["value"]
        low = r["low"]
        high = r["high"]

        if status == "CRITICAL":
            if value < low:
                summary.append(
                    f"🚨 {test} is critically low ({value}, normal range: {low}-{high})."
                )
            else:
                summary.append(
                    f"🚨 {test} is critically high ({value}, normal range: {low}-{high})."
                )
        elif status == "HIGH":
            summary.append(
                f"⚠️ {test} is elevated ({value}, normal range: {low}-{high})."
            )
        elif status == "SLIGHTLY_ABNORMAL":
            if value < low:
                summary.append(
                    f"⚠️ {test} is slightly low ({value}, normal range: {low}-{high})."
                )
            else:
                summary.append(
                    f"⚠️ {test} is slightly elevated ({value}, normal range: {low}-{high})."
                )

    if len(summary) == 0:
        return "✅ All values appear within normal range."

    return " ".join(summary)