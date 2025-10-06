import json
import unittest

# Run tests from project root
# python -m scripts.tests.test_extract_population_actual

from scripts.extract_population_actual import parse_count, validate_scoring, convert_results_to_rows, load_measure_sections, MeasureSection, capture_results

class TestExtractPopulationActual(unittest.TestCase):

    def test_parse_count_true_returns_1(self):
        """Test for parse_count returns 1 for true"""
        self.assertEqual(parse_count('true'), 1)
        self.assertEqual(parse_count('True'), 1)
        self.assertEqual(parse_count('TRUE'), 1)
    
    def test_parse_count_false_returns_0(self):
        """Test for parse_count returns 0 for false"""
        self.assertEqual(parse_count('false'), 0)
        self.assertEqual(parse_count('False'), 0)
        self.assertEqual(parse_count('FALSE'), 0)

    def test_validate_scoring_denom_true_numer_true_then_numer_true(self):
        populations = {
            'Denominator': 1,
            'Numerator': 1
        }
        validate_scoring(populations)
        self.assertEqual(populations['Denominator'], 1)
        self.assertEqual(populations['Numerator'], 1)

    def test_validate_scoring_denom_false_numer_true_then_numer_false(self):
        populations = {
            'Denominator': 0,
            'Numerator': 1
        }
        validate_scoring(populations)
        self.assertEqual(populations['Denominator'], 0)
        self.assertEqual(populations['Numerator'], 0)

    def test_validate_scoring_denom_true_denex_false_numer_true_then_numer_true(self):
        populations = {
            'Denominator': 1,
            'Denominator Exclusion': 0,
            'Numerator': 1
        }
        validate_scoring(populations)
        self.assertEqual(populations['Denominator'], 1)
        self.assertEqual(populations['Denominator Exclusion'], 0)
        self.assertEqual(populations['Numerator'], 1)

    def test_validate_scoring_denom_true_denex_true_numer_true_then_denom_false_numer_false(self):
        populations = {
            'Denominator': 1,
            'Denominator Exclusion': 1,
            'Numerator': 1
        }
        validate_scoring(populations)
        self.assertEqual(populations['Denominator'], 0)
        self.assertEqual(populations['Denominator Exclusion'], 1)
        self.assertEqual(populations['Numerator'], 0)

    def test_validate_scoring_denom_true_numer_true_numex_true_then_numer_false(self):
        populations = {
            'Denominator': 1,
            'Numerator': 1,
            'Numerator Exclusion': 1,
        }
        validate_scoring(populations)
        self.assertEqual(populations['Denominator'], 1)
        self.assertEqual(populations['Numerator'], 0)
        self.assertEqual(populations['Numerator Exclusion'], 1)

    def test_validate_scoring_denom_true_numer_true_denexp_true_then_denom_true(self):
        populations = {
            'Denominator': 1,
            'Denominator Exception': 1,
            'Numerator': 1,
        }
        validate_scoring(populations)
        self.assertEqual(populations['Denominator'], 1)
        self.assertEqual(populations['Denominator Exception'], 0)
        self.assertEqual(populations['Numerator'], 1)

    def test_convert_results_to_rows(self):
        results = {
            'measureA': {
                'p101': {
                    'denom': 1,
                    'numer': 1,
                },
                'p102': {
                    'denom': 0,
                    'numer': 0,
                }
            },
            'measureB': {
                'p201': {
                    'denom': 1,
                    'numer': 0,
                }
            }
        }

        expected_rows = [
            ['measureA', 'p101', 'denom', 1],
            ['measureA', 'p101', 'numer', 1],
            ['measureA', 'p102', 'denom', 0],
            ['measureA', 'p102', 'numer', 0],
            ['measureB', 'p201', 'denom', 1],
            ['measureB', 'p201', 'numer', 0],
        ]

        actual_rows = convert_results_to_rows(results)
        self.assertEqual(expected_rows, actual_rows)

    def test_load_measure_sections(self):
        with open('./scripts//tests/resources/sample_results/.load_measure_expected_results.json', 'r') as file:
            expected_sections = json.load(file)

        for measure_section in load_measure_sections('./scripts/tests/resources/sample_results'):
            self.assertIn(measure_section.section, expected_sections[measure_section.measure])
            
            # remove the section from the list, 
            # later will check that the expected list is empty
            # this will prove all expected items were found
            expected_sections[measure_section.measure].remove(measure_section.section)
            if not expected_sections[measure_section.measure]:
                expected_sections.pop(measure_section.measure)
        
        self.assertFalse(expected_sections)

    def test_capture_results(self):
        with open('./scripts/tests/resources/sample_results/.capture_results_expected.json', 'r') as file:
            expected_results = json.load(file)

        actual_results = capture_results(load_measure_sections('./scripts/tests/resources/sample_results'))
        self.assertDictEqual(expected_results, actual_results)

if __name__ == '__main__':
    unittest.main()