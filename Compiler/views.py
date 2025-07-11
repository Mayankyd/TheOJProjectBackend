from django.shortcuts import render
from django.http import HttpResponse
from .forms import CodeSubmissionForm
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Problem, TestCase
from .serializers import ProblemSerializer


@api_view(['GET'])
def problem_list(request):
    problems = Problem.objects.all()
    serializer = ProblemSerializer(problems, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def submit(request):
    try:
        data = request.data
        language = data.get("language")
        code = data.get("code")
        problem_id = data.get("problem_id")
        mode = data.get("mode")

        # Validation
        if not all([language, code, problem_id, mode]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        test_cases = TestCase.objects.filter(problem_id=problem_id)

        if not test_cases.exists():
            return Response({"error": "No test cases found for this problem"}, status=status.HTTP_404_NOT_FOUND)

        # Mode-based filtering
        if mode == "run":
            test_cases = test_cases[:1]  # Only first test case
        elif mode == "submit":
            test_cases = test_cases      # All test cases
        else:
            return Response({"error": "Invalid mode. Use 'run' or 'submit'."}, status=status.HTTP_400_BAD_REQUEST)

        # Execute
        results = run_code(language, code, test_cases)
        return Response(results)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.http import JsonResponse

def test_submit(request):
    return JsonResponse({'message': 'Compiler API is working!'})


def run_code(language, code, test_cases):
    from pathlib import Path
    import subprocess
    import uuid
    import os
    from django.conf import settings

    project_path = Path(settings.BASE_DIR) / "Compiler"
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())
    code_file_name = f"{unique}.{language}"
    code_file_path = codes_dir / code_file_name

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    results = []

    for idx, test in enumerate(test_cases):  # 🛠 Enumerate to separate file per test
        input_data = test.input_data.strip() + '\n'
        expected_output = test.expected_output.strip()

        input_file_name = f"{unique}_input_{idx}.txt"
        output_file_name = f"{unique}_output_{idx}.txt"

        input_file_path = inputs_dir / input_file_name
        output_file_path = outputs_dir / output_file_name

        with open(input_file_path, "w") as input_file:
            input_file.write(input_data)

        with open(output_file_path, "w") as output_file:
            pass

        try:
            if language == "cpp":
                executable_path = codes_dir / unique
                compile_result = subprocess.run(
                    ["g++", str(code_file_path), "-o", str(executable_path) + ".exe"],
                    capture_output=True,
                    text=True
                )
                if compile_result.returncode == 0:
                    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                        subprocess.run(
                            [str(executable_path) + ".exe"],
                            stdin=input_file,
                            stdout=output_file,
                            stderr=subprocess.PIPE,
                            check=True
                        )
                else:
                    return {'status': 'Compilation Error', 'error': compile_result.stderr}

            elif language == "py":
                with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                    subprocess.run(
                        ["python", str(code_file_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,
                        check=True
                    )

            elif language == "java":
                java_file_path = codes_dir / "Main.java"
                with open(java_file_path, "w") as code_file:
                    code_file.write(code)

                compile_result = subprocess.run(
                    ["javac", str(java_file_path)],
                    capture_output=True,
                    text=True
                )

                if compile_result.returncode == 0:
                    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                        subprocess.run(
                            ["java", "-cp", str(codes_dir), "Main"],
                            stdin=input_file,
                            stdout=output_file,
                            stderr=subprocess.PIPE,
                            text=True,
                            check=True
                        )
                else:
                    return {'status': 'Compilation Error', 'error': compile_result.stderr}

        except subprocess.CalledProcessError as e:
            return {'status': 'Runtime Error', 'error': e.stderr.decode()}

        with open(output_file_path, "r") as output_file:
            actual_output = output_file.read().strip()

        if actual_output == expected_output:
            results.append({
                'input': test.input_data,
                'expected': expected_output,
                'actual': actual_output,
                'status': 'Passed'
            })
        else:
            results.append({
                'input': test.input_data,
                'expected': expected_output,
                'actual': actual_output,
                'status': 'Failed'
            })

    all_passed = all(r["status"] == "Passed" for r in results)
    return {
        'status': 'Accepted' if all_passed else 'Wrong Answer',
        'details': results
    }
