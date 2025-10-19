import os
import csv
import glob
from collections import namedtuple
from datetime import datetime
from typing import Dict, List, NamedTuple, Set, Tuple, TypedDict

MeasureDifference = namedtuple('MeasureDifference', ['measure', 'total_test_cases', 'test_cases_with_differences', 'result_deltas'])
ResultKey = namedtuple('ResultKey', ['measure_name', 'patient_guid', 'group'])
ResultDelta = namedtuple('ResultDelta', ['patient_guid', 'group', 'population', 'expected', 'actual'])

class MissingPopulation(NamedTuple):
    result_key: ResultKey
    population: List[str]

class Discrepancies(NamedTuple):
    missing_results: List[ResultKey]
    missing_populations: List[MissingPopulation]
    population_differences: Dict[str, List[str]]
    measures_with_discrepancies: Set[str]

class Results(NamedTuple):
    rows: Dict[str, str]
    groups: Dict[ResultKey, Dict[str, str]]

def capture_results(file: str) -> Results:
    rows = {}
    results = {}
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["measure_name"], row["guid"], row["population"])
            rows[key] = row["count"]

            group_and_population = row["population"].split(':')
            result_key = ResultKey(row["measure_name"], row["guid"], group_and_population[0])
            result = results.setdefault(result_key, {})
            result[group_and_population[1]] = row["count"]
    return Results(rows, results)

def generate_output(file: str, expected_rows: Dict, actual_rows: Dict) -> Tuple[int, int]:
    header = ["result", "measure_name", "guid", "population", "expected_result", "actual_result"]
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

def create_markdown_table(headers: List[str], data: List[str]) -> List[str]:
    table_rows = []

    # header row
    table_rows.append(f'| {" | ".join(headers)} |\n')

    # separator row
    table_rows.append(f'| {" | ".join(["---"] * len(headers))} |\n')

    # data rows
    for row_data in data:
        table_rows.append("| " + " | ".join(map(str, row_data)) + " |\n")
    table_rows.append('\n\n')
    return table_rows

def cql_file_link(measure_name: str) -> str:
    return f'[{measure_name}](../../input/cql/{measure_name}.cql)'

def measure_report_file_link(measure_name: str, patient_guid: str) -> str:
    # path relative to root directory, this is the expected location for running the script
    measure_dir = f'./input/tests/measure/{measure_name}/{patient_guid}/'
    measure_report_file = glob.glob(f'{measure_dir}/MeasureReport*.json')
    if measure_report_file:
        # path relative to this script, need to add parent directories
        return f'[{patient_guid}](../../{measure_report_file[0]})'
    else:
        return patient_guid[1]

def test_results_file_link(measure_name: str) -> str:
    return f'[{measure_name}](../../input/tests/results/{measure_name}.txt)'

def test_case_count(measure_name: str) -> int:
    # path relative to root directory, this is the expected location for running the script
    test_case_dir = f'./input/tests/measure/{measure_name}/'
    files_in_test_case_dir = os.listdir(test_case_dir)
    sub_dirs = [item for item in files_in_test_case_dir if os.path.isdir(os.path.join(test_case_dir, item))]
    return len(sub_dirs)

def measure_count(measure_results: List[ResultKey]) -> int:
    return len(set([result_key.measure_name for result_key in measure_results]))

def test_case_count(measure_results: List[ResultKey]) -> int:
    return len(set([(result_key.measure_name, result_key.patient_guid) for result_key in measure_results]))

def link_from_count(measure: str, count: int) -> str:
    f'[{measure}](#measure-{measure.lower()})' if measure in measures_with_discrepancies and count > 0 else measure,

def capture_discrepancies(expected_results: Dict[ResultKey, Dict[str, str]], actual_results: Dict[ResultKey, Dict[str, str]]) -> Discrepancies:
    missing_results = []
    missing_populations = []
    population_differences = {}
    measures_with_discrepancies = set()
    for expected_results_key, expected_populations in expected_results.items():
        if expected_results_key not in actual_results:
            missing_results.append(expected_results_key)
            measures_with_discrepancies.add(expected_results_key.measure_name)
        else:
            actual_populations = actual_results[expected_results_key]
            # confirm all expected populations exist
            population_delta = list(set(expected_populations.keys()) - set(actual_populations.keys()))
            if population_delta:
                missing_populations.append(MissingPopulation(expected_results_key, population_delta))
                measures_with_discrepancies.add(expected_results_key.measure_name)
            else:
                mismatched_populations = [
                    ResultDelta(expected_results_key.patient_guid, 
                     expected_results_key.group, 
                     population,
                     expected_populations[population], 
                     actual_populations[population])
                     for population in expected_populations.keys() & actual_populations.keys() if expected_populations[population] != actual_populations[population]]
                if mismatched_populations:
                    measures_with_discrepancies.add(expected_results_key.measure_name)
                    population_differences.setdefault(expected_results_key.measure_name, []) 
                    population_differences[expected_results_key.measure_name] = population_differences[expected_results_key.measure_name] + mismatched_populations
    return Discrepancies(missing_results, missing_populations, population_differences, measures_with_discrepancies)

def group_discrepancies_by_measure(expected_results: Dict[ResultKey, Dict[str, str]], discrepancies: Discrepancies) -> List[List]:
    measure_results = []
    for expected_measure_name in [measure_name for measure_name in sorted(list(set([k.measure_name for k in expected_results.keys()]))) if measure_name in discrepancies.measures_with_discrepancies]:
        measure_results.append([
            f'[{expected_measure_name}](#measure-{expected_measure_name.lower()})' if expected_measure_name in discrepancies.measures_with_discrepancies else expected_measure_name,
            len(set([result_key.patient_guid for result_key in expected_results.keys() if result_key.measure_name == expected_measure_name])),
            len(set([result_key.patient_guid for result_key in discrepancies.missing_results if result_key.measure_name == expected_measure_name])),
            len(set([result_key.patient_guid for (result_key, _) in discrepancies.missing_populations if result_key.measure_name == expected_measure_name])),
            len(discrepancies.population_differences.get(expected_measure_name, {}))])
    return measure_results

def generate_comparison_report(file: str, expected_results: Dict[ResultKey, Dict[str, str]], actual_results: Dict[ResultKey, Dict[str, str]]):
    discrepancies = capture_discrepancies(expected_results, actual_results)

    total_measure_count = measure_count(expected_results.keys())
    total_test_case_count = test_case_count(expected_results.keys())
    with open(file, "w", newline="") as f:
        f.write('## Comparison Report\n')
        f.write(f'Generated: {datetime.now()}\n')
        f.write(f'Total Measures: {len(set([result_key.measure_name for result_key in expected_results.keys()]))}\n')
        f.write(f'Total Test Cases: {len(set([(result_key.measure_name, result_key.patient_guid) for result_key in expected_results.keys()]))}\n')
        f.write(f'Measures with Discrepancies: {len(discrepancies.measures_with_discrepancies)}\n')
        f.write('\n\n')

        discrepancies_by_measure = group_discrepancies_by_measure(expected_results, discrepancies)
        if discrepancies_by_measure:
            f.write(f'### Measures with Discrepancies ({len(discrepancies_by_measure)} test cases)\n')
            f.writelines(create_markdown_table(
                ['Measure', 'Total Test Cases', 'Missing Results', 'Missing Populations', 'Mismatched Test Cases'],
                group_discrepancies_by_measure(expected_results, discrepancies)))
        
        if discrepancies.missing_results:
            f.write(f'### Missing Results ({len(discrepancies.missing_results)} test cases)\n')
            f.writelines(create_markdown_table(
                ['CQL', 'Test Case', 'Group'],
                [[cql_file_link(missing_id[0]),
                  measure_report_file_link(missing_id[0], missing_id[1]),  
                  missing_id[2]] for missing_id in discrepancies.missing_results]))
        
        if discrepancies.missing_populations:
            f.write(f'### Missing Populations ({len(discrepancies.missing_populations)} test cases)\n')
            f.writelines(create_markdown_table(
                ['CQL', 'Test Case', 'Test Results', 'Group', 'Population'],
                [[cql_file_link(missing_id[0]),
                  measure_report_file_link(missing_id[0], missing_id[1]),
                  test_results_file_link(missing_id[0]),
                  missing_id[2],
                  ','.join(populations)] for (missing_id, populations) in discrepancies.missing_populations]))
        
        if discrepancies.population_differences:
            f.write(f'### Different Measure Results ({len(discrepancies.population_differences)} of {total_measure_count} measures)\n')
            for (measure, differences) in discrepancies.population_differences.items():
                f.write(f'##### Measure: {cql_file_link(measure)}\n')
                f.write(f'Test Results: {test_results_file_link(measure)}\n')
                f.writelines(create_markdown_table(
                    ['Test Case', 'Group', 'Population', 'Expected', 'Actual'],
                    [[measure_report_file_link(measure, result_delta.patient_guid),
                      result_delta.group,
                      result_delta.population,
                      result_delta.expected,
                      result_delta.actual] for result_delta in differences]))

def main(expected_file: str, actual_file: str, output_file: str, comparison_report: str):
    expected_results = capture_results(expected_file)
    actual_results = capture_results(actual_file)
    
    # pass_fail_count = generate_output(output_file, expected_results[0], actual_results[0])
    # pass_pct = pass_fail_count[0] / (pass_fail_count[0] + pass_fail_count[1]) * 100
    # print(f"PASS: {pass_fail_count[0]} ({pass_pct:.2f})%")
    # print(f"FAIL: {pass_fail_count[1]} ({(100 - pass_pct):.2f})%")
    
    generate_comparison_report(comparison_report, expected_results[1], actual_results[1])

if __name__ == '__main__':
    expected_file = "./scripts/comparison/expected_results.csv"
    actual_file = "./scripts/comparison/actual_results.csv"
    output_file = "./scripts/comparison/output_results.csv"
    comparison_report = "./scripts/comparison/comparison_report.md"

    main(expected_file, actual_file, output_file, comparison_report)
