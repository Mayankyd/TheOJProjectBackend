from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path
import re
import requests
from dotenv import load_dotenv

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Problem, TestCase
from .serializers import ProblemSerializer
from django.views.decorators.csrf import csrf_exempt 

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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

        if not all([language, code, problem_id, mode]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        test_cases = TestCase.objects.filter(problem_id=problem_id)

        if not test_cases.exists():
            return Response({"error": "No test cases found for this problem"}, status=status.HTTP_404_NOT_FOUND)

        if mode == "run":
            test_cases = test_cases[:1]
        elif mode != "submit":
            return Response({"error": "Invalid mode. Use 'run' or 'submit'."}, status=status.HTTP_400_BAD_REQUEST)

        results = run_code(language, code, test_cases)
        results['code'] = code  # send code in response if failed
        results['problem_id'] = problem_id
        return Response(results)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def ai_syntax_suggest(request):
    try:
        code_snippet = request.data.get("code_snippet", "").strip()
        language = request.data.get("language", "").strip()

        if not code_snippet or not language:
            return Response({"error": "Missing code_snippet or language"}, status=400)

        prompt = f"Provide only the syntax for this {language} code fragment:\n\n{code_snippet}"

        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        response = requests.post(endpoint, headers=headers, json=data)
        if response.status_code != 200:
            return Response({"error": response.json()}, status=response.status_code)

        result = response.json()
        raw_suggestion = result["candidates"][0]["content"]["parts"][0]["text"].strip()

        suggestion = re.sub(r"```[a-z]*", "", raw_suggestion)
        suggestion = suggestion.replace("```", "").strip()

        return Response({"suggestion": suggestion}, status=200)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=500)

@csrf_exempt
@api_view(['POST'])
def ai_hint(request):
    try:
        code = request.data.get("code", "").strip()
        problem_id = request.data.get("problem_id")

        if not code or not problem_id:
            return Response({"hint": None, "error": "Missing code or problem_id"}, status=400)

        # Optional: Fetch problem text from DB if needed
        # For now, prompt without that:
        prompt = f"""A user has written the following code which is incorrect. Give a helpful hint (not full solution) to improve it.
        
Problem ID: {problem_id}
User Code:
{code}

Respond with only one clear hint.
"""

        endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        response = requests.post(endpoint, headers=headers, json=data)
        if response.status_code != 200:
            return Response({"hint": None, "error": response.json()}, status=response.status_code)

        result = response.json()
        raw_hint = result["candidates"][0]["content"]["parts"][0]["text"].strip()

        # Remove markdown or code formatting if present
        cleaned_hint = re.sub(r"```[a-z]*", "", raw_hint).replace("```", "").strip()

        return Response({"hint": cleaned_hint}, status=200)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"hint": None, "error": str(e)}, status=500)


def test_submit(request):
    return JsonResponse({'message': 'Compiler API is working!'})


def run_code(language, code, test_cases):
    project_path = Path(settings.BASE_DIR) / "Compiler"
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
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

    for idx, test in enumerate(test_cases):
        input_data = test.input_data.strip() + '\n'
        expected_output = test.expected_output.strip()

        input_file_path = inputs_dir / f"{unique}_input_{idx}.txt"
        output_file_path = outputs_dir / f"{unique}_output_{idx}.txt"

        with open(input_file_path, "w") as f:
            f.write(input_data)
        with open(output_file_path, "w"):
            pass

        try:
            if language == "cpp":
                executable_path = codes_dir / unique
                compile_result = subprocess.run(
                    ["g++", str(code_file_path), "-o", str(executable_path) + ".exe"],
                    capture_output=True, text=True
                )
                if compile_result.returncode == 0:
                    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                        subprocess.run(
                            [str(executable_path) + ".exe"],
                            stdin=input_file, stdout=output_file,
                            stderr=subprocess.PIPE, check=True
                        )
                else:
                    return {'status': 'Compilation Error', 'error': compile_result.stderr}

            elif language == "py":
                with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                    subprocess.run(
                        ["python", str(code_file_path)],
                        stdin=input_file, stdout=output_file,
                        stderr=subprocess.PIPE, check=True
                    )

            elif language == "java":
                java_file_path = codes_dir / "Main.java"
                with open(java_file_path, "w") as code_file:
                    code_file.write(code)
                compile_result = subprocess.run(
                    ["javac", str(java_file_path)],
                    capture_output=True, text=True
                )
                if compile_result.returncode == 0:
                    with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                        subprocess.run(
                            ["java", "-cp", str(codes_dir), "Main"],
                            stdin=input_file, stdout=output_file,
                            stderr=subprocess.PIPE, text=True, check=True
                        )
                else:
                    return {'status': 'Compilation Error', 'error': compile_result.stderr}

        except subprocess.CalledProcessError as e:
            return {'status': 'Runtime Error', 'error': e.stderr.decode()}

        with open(output_file_path, "r") as output_file:
            actual_output = output_file.read().strip()

        results.append({
            'input': test.input_data,
            'expected': expected_output,
            'actual': actual_output,
            'status': 'Passed' if actual_output == expected_output else 'Failed'
        })

    # ✅ Moved outside the loop
    all_passed = all(r["status"] == "Passed" for r in results)
    final_status = 'Accepted' if all_passed else 'Wrong Answer'

    return {
        'status': final_status,
        'details': results,
        'wrong_code': code if final_status == "Wrong Answer" else None
    }


