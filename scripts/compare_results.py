import csv
from typing import Tuple, Dict

def capture_results(file: str) -> Tuple[Dict, Dict]:
    rows = {}
    results = {}
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["measure_name"], row["guid"], row["population"])
            rows[key] = row["count"]

            result_key = (row["measure_name"], row["guid"])
            results = results.setdefault(result_key, {})
            results[row["display_name"]] = row["count"]
    return (rows, results)

def generate_output(file: str, expected_rows: Dict, actual_rows: Dict) -> Tuple[int, int]:
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

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(output)

    return (pass_count, fail_count)

def main(expected_file: str, actual_file: str, output_file: str, comparison_report: str):
    expected_results = capture_results(expected_file)
    actual_results = capture_results(actual_file)
    
    pass_fail_count = generate_output(output_file, expected_results[0], actual_results[0])
    pass_pct = pass_fail_count[0] / (pass_fail_count[0] + pass_fail_count[1]) * 100
    print(f"PASS: {pass_fail_count[0]} ({pass_pct:.2f})%")
    print(f"FAIL: {pass_fail_count[1]} ({(100 - pass_pct):.2f})%")

if __name__ == '__main__':
    expected_file = "./scripts/comparison/expected_results.csv"
    actual_file = "./scripts/comparison/actual_results.csv"
    output_file = "./scripts/comparison/output_results.csv"
    comparison_report = "./scripts/comparison/comparison_report.md"

    main(expected_file, actual_file, output_file, comparison_report)
