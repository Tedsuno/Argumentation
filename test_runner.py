import subprocess

# Liste des tests avec commande, sortie attendue
tests = [
    {
        "command": "python3 project.py -p SE-CO -f test_af1.apx",
        "expected_output": """Complete extensions:
[[], ['B', 'D'], ['A', 'D']]"""
    },
    {
        "command": "python3 project.py -p SE-ST -f test_af1.apx",
        "expected_output": """Stable extensions:
[['B', 'D'], ['A', 'D']]"""
    },
    {
        "command": "python3 project.py -p DC-CO -f test_af1.apx -a A",
        "expected_output": "Credulously accepted arguments:\nA"
    },
    {
        "command": "python3 project.py -p DC-CO -f test_af1.apx -a B",
        "expected_output": "Credulously accepted arguments:\nB"
    },
    {
        "command": "python3 project.py -p DC-CO -f test_af1.apx -a C",
        "expected_output": "Credulously accepted arguments:\nC"
    },
    {
        "command": "python3 project.py -p DC-CO -f test_af1.apx -a D",
        "expected_output": "Credulously accepted arguments:\nD"
    },
    {
        "command": "python3 project.py -p DC-CO -f test_af1.apx -a E",
        "expected_output": "Credulously accepted arguments:\nE"
    },
    {
        "command": "python3 project.py -p DS-CO -f test_af1.apx -a A",
        "expected_output": "Skeptically accepted arguments:\nA"
    },
    {
        "command": "python3 project.py -p DS-CO -f test_af1.apx -a B",
        "expected_output": "Skeptically accepted arguments:\nB"
    },
    {
        "command": "python3 project.py -p DS-CO -f test_af1.apx -a C",
        "expected_output": "Skeptically accepted arguments:\nC"
    },
    {
        "command": "python3 project.py -p DS-CO -f test_af1.apx -a D",
        "expected_output": "Skeptically accepted arguments:\nD"
    },
    {
        "command": "python3 project.py -p DS-CO -f test_af1.apx -a E",
        "expected_output": "Skeptically accepted arguments:\nE"
    },
    {
        "command": "python3 project.py -p DC-ST -f test_af1.apx -a A",
        "expected_output": "Credulously accepted arguments:\nA"
    },
    {
        "command": "python3 project.py -p DC-ST -f test_af1.apx -a D",
        "expected_output": "Credulously accepted arguments:\nD"
    },
    {
        "command": "python3 project.py -p DS-ST -f test_af1.apx -a A",
        "expected_output": "Skeptically accepted arguments:\nA"
    },
    {
        "command": "python3 project.py -p DS-ST -f test_af1.apx -a D",
        "expected_output": "Skeptically accepted arguments:\nD"
    }
]

def parse_and_sort_sets(output):
    """
    Parse les ensembles dans une sortie, les trie individuellement et globalement.
    """
    lines = output.strip().split("\n")
    parsed_sets = []
    for line in lines:
        if line.startswith("[") and line.endswith("]"):
            try:
                parsed_sets = eval(line)  # Interprète la ligne contenant les ensembles comme une liste Python
                break
            except:
                continue
    if isinstance(parsed_sets, list):
        return [sorted(ext) for ext in parsed_sets]
    return parsed_sets

def compare_outputs_unordered(expected, actual):
    """
    Compare expected and actual outputs by ensuring each actual set matches an expected set, ignoring order.
    """
    expected_sets = parse_and_sort_sets(expected)
    actual_sets = parse_and_sort_sets(actual)

    if not isinstance(expected_sets, list) or not isinstance(actual_sets, list):
        return expected.strip() == actual.strip()

    # Convert lists of lists into sets of tuples pour comparaison
    expected_sets = {tuple(sorted(ext)) for ext in expected_sets}
    actual_sets = {tuple(sorted(ext)) for ext in actual_sets}

    return expected_sets == actual_sets

def run_test(test):
    """
    Exécute un test, compare la sortie réelle avec la sortie attendue et retourne le résultat.
    """
    command = test["command"]
    expected_output = test["expected_output"]

    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        actual_output = result.stdout.strip()

        # Compare les résultats
        if compare_outputs_unordered(expected_output, actual_output):
            return True, actual_output
        else:
            return False, f"Expected: {expected_output}\nActual: {actual_output}"
    except Exception as e:
        return False, str(e)

# Exécution des tests
total_tests = len(tests)
passed_tests = 0
failed_tests = []

for test in tests:
    success, output = run_test(test)
    if success:
        passed_tests += 1
        print(f"✔ Test Passed: {test['command']} \n  Output: {output}")
    else:
        failed_tests.append({"command": test["command"], "error": output})
        print(f"✘ Test Failed: {test['command']} \n  Error: {output}")

# Résumé des résultats
print("\nTest Summary:")
print(f"Total Tests: {total_tests}")
print(f"Passed: {passed_tests}")
print(f"Failed: {len(failed_tests)}")

if failed_tests:
    print("\nFailed Tests Details:")
    for fail in failed_tests:
        print(f"Command: {fail['command']}")
        print(f"Error: {fail['error']}")
        print("----------------------------------------")
