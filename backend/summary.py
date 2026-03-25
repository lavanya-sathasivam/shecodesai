def generate_summary(results):

    summary=[]

    for r in results:

        if r["status"]=="LOW":

            summary.append(
            f"{r['test']} is lower than the normal range."
            )

        elif r["status"]=="HIGH":

            summary.append(
            f"{r['test']} is higher than normal which may indicate infection or disease."
            )

    if len(summary)==0:

        return "All values appear within normal range."

    return " ".join(summary)