import pandas as pd

# Load datasets
lab = pd.read_csv(r"C:\Users\lavan\Desktop\shecodesai\dataset\blood_count_dataset.csv")
med = pd.read_csv(r"C:\Users\lavan\Desktop\shecodesai\dataset\medicine_dataset.csv", low_memory=False)

# -------------------------
# Extract lab test names
# -------------------------

# Remove non-test columns
lab_columns = list(lab.columns)

remove_cols = ["Age", "Gender"]

lab_tests = [col for col in lab_columns if col not in remove_cols]

lab_df = pd.DataFrame({
    "name": lab_tests,
    "type": "lab_test"
})

# -------------------------
# Extract medicine names
# -------------------------

med_df = pd.DataFrame({
    "name": med["name"],
    "type": "medicine"
})

# -------------------------
# Combine datasets
# -------------------------

combined = pd.concat([lab_df, med_df])

# Remove duplicates
combined = combined.drop_duplicates()

# Save knowledge base
combined.to_csv(
r"C:\Users\lavan\Desktop\shecodesai\dataset\medical_knowledge_base.csv",
index=False
)

print("Medical knowledge base created successfully!")