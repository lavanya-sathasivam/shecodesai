import pandas as pd

# Load reference ranges
ranges = pd.read_csv("dataset/reference_ranges.csv")


def check_critical_alerts(abnormal_results):

    alerts = []

    for result in abnormal_results:

        test = result.get("test")
        value = result.get("value")
        status = result.get("status")

        if status == "CRITICAL":

            message = f"🚨 CRITICAL ALERT: {test} is dangerously abnormal (value: {value}). Please consult a doctor immediately."

            alerts.append(message)

    return alerts


# -------------------------------------
# Advanced alert system (risk-based)
# -------------------------------------

def generate_medical_alerts(values):

    alerts = []

    # Example rule-based alerts
    if "Hemoglobin" in values:

        if values["Hemoglobin"] < 8:
            alerts.append(
                "🚨 Severe anemia detected. Immediate medical attention required."
            )

    if "White_Blood_Cells" in values:

        if values["White_Blood_Cells"] > 15000:
            alerts.append(
                "⚠ Possible severe infection detected."
            )

    if "Platelet_Count" in values:

        if values["Platelet_Count"] < 50000:
            alerts.append(
                "🚨 Platelet count dangerously low. Risk of bleeding."
            )

    if "Glucose" in values:

        if values["Glucose"] > 200:
            alerts.append(
                "⚠ High glucose detected. Possible uncontrolled diabetes."
            )

    return alerts