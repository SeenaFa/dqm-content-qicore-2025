import os
import re
import csv

results_dir = "./input/tests/results"
output_file = "./scripts/comparison/actual_results.csv"

header = ["measure_name", "guid", "display_name", "count"]
rows = []

allowed_display_names = {
    "Initial Population",
    "Denominator",
    "Denominator Exclusion",
    "Denominator Exclusions",
    "Denominator Exception",
    "Denominator Exceptions",
    "Numerator",
    "Numerator Exclusion",
    "Numerator Exclusions",
    "Numerator Excpetion",
    "Numerator Excpetions",
    "Measure Observation",
    "Measure Observations",
    "Measure Population",
    "Measure Population Observation",
    "Measure Population Observations",
    "Measure Population Exclusion",
    "Measure Population Exclusions"
}

def parse_count(result_value):
    result_value = result_value.strip()
    if result_value.lower() == "true":
        return 1
    elif result_value.lower() == "false":
        return 0
    elif result_value.startswith("[") and result_value.endswith("]"):
        items = [item.strip() for item in result_value[1:-1].split(",") if item.strip()]
        return len(items)
    else:
        return result_value  # fallback, could be a number or string

for file_name in os.listdir(results_dir):
    # Skip hidden/system files like .DS_Store
    if file_name.startswith('.'):
        continue
    file_path = os.path.join(results_dir, file_name)
    if os.path.isfile(file_path):
        measure_name = os.path.splitext(file_name)[0]
        print("Parsing Measure results:", measure_name)
        with open(file_path, "r") as f:
            content = f.read()
        # Split sections by two line breaks instead of hyphens
        sections = re.split(r'\n\s*\n', content)
        for section in sections:
            guid_match = re.search(r'Patient\s*=\s*Patient\(id=([a-f0-9\-]+)\)', section)
            guid = guid_match.group(1) if guid_match else ""
            for line in section.splitlines():
                if "=" in line:
                    parts = line.split("=", 1)
                    display_name = parts[0].strip()
                    result_value = parts[1].strip()
                    if display_name in allowed_display_names:
                        count = parse_count(result_value)
                        if guid and display_name:
                            rows.append([measure_name, guid, display_name, count])

os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)