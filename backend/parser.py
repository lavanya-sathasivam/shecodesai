import re

def extract_lab_values(text):

    pattern = r'([A-Za-z_]+)\s*[:\-]?\s*(\d+\.?\d*)'

    matches = re.findall(pattern, text)

    values = {}

    for test,value in matches:

        values[test] = float(value)

    return values