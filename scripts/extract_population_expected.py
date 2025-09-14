import os
import json
import csv

base_dir = "./input/tests/measure"
measure_resource_dir = "./input/resources/measure"
output_file = "./scripts/comparison/expected_results.csv"

header = ["measure_name", "guid", "display_name", "count"]
rows = []

# Preload all measure resources and index population criteria by code
measure_criteria_map = {}
for measure_file in os.listdir(measure_resource_dir):
    if measure_file.endswith(".json"):
        measure_path = os.path.join(measure_resource_dir, measure_file)
        print("Parsing Measure resource:", measure_path)
        with open(measure_path, "r") as f:
            measure_data = json.load(f)
            measure_name = os.path.splitext(measure_file)[0]
            for group in measure_data.get("group", []):
                for pop in group.get("population", []):
                    code = pop.get("code", {}).get("coding", [{}])[0].get("code", "")
                    criteria = pop.get("criteria", {}).get("expression", "")
                    # Index by measure_name and code
                    measure_criteria_map[(measure_name, code)] = criteria

for measure_name in os.listdir(base_dir):
    measure_path = os.path.join(base_dir, measure_name)
    if os.path.isdir(measure_path):
        for root, _, files in os.walk(measure_path):
            for file in files:
                if file.startswith("MeasureReport-") and file.endswith(".json"):
                    guid = os.path.basename(root)
                    file_path = os.path.join(root, file)
                    print("Parsing MeasureReport resource:", file_path)
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        for group in data.get("group", []):
                            for pop in group.get("population", []):
                                code = pop.get("code", {}).get("coding", [{}])[0].get("code", "")
                                # Get display name from measure resource criteria.expression
                                display = measure_criteria_map.get((measure_name, code), "")
                                count = pop.get("count", "")
                                rows.append([measure_name, guid, display, count])

os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)