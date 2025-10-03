import os
import re
import csv
from collections import namedtuple
from typing import Generator, List, Dict, Union

MeasureSection = namedtuple('MeasureSection', ['measure', 'section'])

header = ["measure_name", "guid", "display_name", "count"]

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
    "Numerator Exception",
    "Numerator Exceptions",
    "Measure Observation",
    "Measure Observations",
    "Measure Population",
    "Measure Population Observation",
    "Measure Population Observations",
    "Measure Population Exclusion",
    "Measure Population Exclusions"
}

patient_pattern = re.compile(r'Patient\s*=\s*Patient\(id=(?P<id>[a-f0-9\-]+)\)')
population_pattern = re.compile(rf'(?P<pop>{"|".join(list(allowed_display_names))})\s*=\s*(?P<value>.*)')
section_pattern = re.compile(r'\n\s*\n')   # Split sections by two line breaks instead of hyphens

def parse_count(result_value: str) -> Union[int, str]:
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

def validate_scoring(populations: Dict[str, str]):
    # scoring validation based on https://build.fhir.org/ig/HL7/cqf-measures/measure-conformance.html#proportion-measure-scoring
    denom = populations.get('Denominator', 0)
    denex = populations.get('Denominator Exclusion', 0)
    denexp = populations.get('Denominator Exception', 0)
    numer = populations.get('Numerator', 0)
    numex = populations.get('Numerator Exclusion', 0)

    if not denom:
        # patient has to first be in the Denominator before they can be in any other population
        denex = 0
        denexp = 0
        numer = 0
        numex = 0
    elif denex:
        # Denominator Exclusion keeps patient out of Denominator and the Denominator Exception
        denom = 0
        denexp = 0

        # Since the patient doesn't make the Denominator, they also cannot be in the Numerator or Numerator Exclusion
        numer = 0
        numex = 0
    elif numer:
        # Numerator keeps the patient out of the Denominator Exception
        denexp = 0
        if numex:
            # Numerator Exclusion keeps the patient out of the Numerator
            numer = 0
    elif denexp:
        # Since the patient didn't make the Numerator,
        # and there is a Denominator Exception the patient can be removed from the Denominator
        denom = 0

    # save updated scoring back to population, but only if the value already existed in the population
    if 'Denominator'in populations:
        populations['Denominator'] = denom
    if 'Denominator Exclusion'in populations:
        populations['Denominator Exclusion'] = denex
    if 'Denominator Exception'in populations:
        populations['Denominator Exception'] = denexp
    if 'Numerator'in populations:
        populations['Numerator'] = numer
    if 'Numerator Exclusion'in populations:
        populations['Numerator Exclusion'] = numex

def load_measure_sections(dir_path: str) -> Generator['MeasureSection', None, None]:
    for file_name in os.listdir(dir_path):
        # Skip hidden/system files like .DS_Store
        if file_name.startswith('.'):
            continue
        print(f' {file_name}')
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            measure_name = os.path.splitext(file_name)[0]
            with open(file_path, "r") as f:
                content = f.read()
            sections = section_pattern.split(content)
            for section in sections:
                yield MeasureSection(measure_name, section)

def capture_results(measure_sections: Generator['MeasureSection', None, None]) -> Dict[str, Dict[str, Dict[str, str]]]:
    # collect results in a dict
    results = {}
    for measure_section in measure_sections:
        section_data = measure_section[1]
        measure_item = results.setdefault(measure_section[0], {})
        guid_match = patient_pattern.search(section_data)
        if guid_match:
            guid = guid_match.group('id')
            section_item = measure_item.setdefault(guid, {})
            for line in section_data.splitlines():
                population_match = population_pattern.search(line)
                if population_match:
                    section_item[population_match.group('pop')] = parse_count(population_match.group('value'))
    return results

def convert_results_to_rows(results: Dict[str, Dict[str, Dict[str, str]]]) -> List[List[str]]:
    # convert results dict to rows
    # during conversion verify that proper proportional eCQM population criteria rules are followed
    rows = []
    for measure, patient_result in results.items():
        for guid, populations in patient_result.items():
            validate_scoring(populations)
            for pop, value in populations.items():
                rows.append([measure, guid, pop, value])
    return rows

def save_results(output_file: str, rows: List[List[str]]):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(rows)

if __name__ == '__main__':
    results_dir = "./input/tests/results"
    output_file = "./scripts/comparison/actual_results.csv"

    print("Loading Measures")
    measure_sections = load_measure_sections(results_dir)

    print("Capturing Results")
    results = capture_results(measure_sections)

    print("Analyzing Results")
    rows = convert_results_to_rows(results)

    print("Saving Results")
    save_results(output_file, rows)
