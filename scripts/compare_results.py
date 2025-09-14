import csv

expected_file = "./scripts/comparison/expected_results.csv"
actual_file = "./scripts/comparison/actual_results.csv"
output_file = "./scripts/comparison/output_results.csv"

expected_rows = {}
with open(expected_file, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["measure_name"], row["guid"], row["display_name"])
        expected_rows[key] = row["count"]

actual_rows = {}
with open(actual_file, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["measure_name"], row["guid"], row["display_name"])
        actual_rows[key] = row["count"]

header = ["result", "measure_name", "guid", "display_name", "expected_result", "actual_result"]
output = []

pass_count = 0
fail_count = 0

for key, expected_result in expected_rows.items():
    actual_result = actual_rows.get(key)
    if actual_result is None or str(expected_result) != str(actual_result):
        output.append(["FAIL", key[0], key[1], key[2], expected_result, actual_result if actual_result is not None else "MISSING"])
        fail_count += 1
    else:
        output.append(["PASS", key[0], key[1], key[2], expected_result, actual_result])
        pass_count += 1

with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(output)

pass_pct = pass_count / (pass_count + fail_count) * 100
print(f"PASS: {pass_count} ({pass_pct:.2f})%")
print(f"FAIL: {fail_count} ({(100 - pass_pct):.2f})%")