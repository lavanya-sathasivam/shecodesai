def calculate_risk_score(results):

    score = 100

    for r in results:

        if r["status"] == "SLIGHTLY_ABNORMAL":
            score -= 5

        if r["status"] == "CRITICAL":
            score -= 15

    if score < 0:
        score = 0

    # Determine health status
    if score >= 85:
        status = "Healthy 🟢"

    elif score >= 60:
        status = "Moderate Risk 🟡"

    else:
        status = "High Risk 🔴"

    return {
        "score": score,
        "status": status
    }