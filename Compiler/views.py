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
from .models import Problem
from .serializers import ProblemSerializer

@api_view(['GET'])
def problem_list(request):
    problems = Problem.objects.all()
    serializer = ProblemSerializer(problems, many=True)
    return Response(serializer.data)

from django.http import JsonResponse

def test_submit(request):
    return JsonResponse({'message': 'Compiler API is working!'})



def submit(request):
    if request.method == "POST":
        print("POST request received")  # ✅
        form = CodeSubmissionForm(request.POST)
        print("Form valid?", form.is_valid())  # ✅
        print("Form data:", request.POST)
        if form.is_valid():
            submission = form.save()
            print(submission.language)
            print(submission.code)
            output = run_code(
                submission.language, submission.code, submission.input_data
            )
            submission.output_data = output
            submission.save()
            return render(request, "Compiler/result.html", {"submission": submission})
    else:
        form = CodeSubmissionForm()
    return render(request, "Compiler/index.html", {"form": form})


def run_code(language, code, input_data):
    from pathlib import Path
    import subprocess
    import uuid
    import os

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
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    # Write the code
    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    # Ensure multi-line input is written correctly
    with open(input_file_path, "w") as input_file:
        input_file.write(input_data.strip() + '\n')

    # Create an empty output file
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
                    run_result = subprocess.run(
                        [str(executable_path) + ".exe"],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,
                        check=True
                    )
            else:
                return f"Compilation Error:\n{compile_result.stderr}"

        elif language == "py":
            with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                run_result = subprocess.run(
                    ["python", str(code_file_path)],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=subprocess.PIPE,
                    check=True
                )

        elif language == "java":
            # Java file must be named Main.java
            java_file_path = codes_dir / "Main.java"

            # Write Java code to Main.java
            with open(java_file_path, "w") as code_file:
                code_file.write(code)

            # Compile Java file
            compile_result = subprocess.run(
                ["javac", str(java_file_path)],
                capture_output=True,
                text=True
            )

            if compile_result.returncode == 0:
                with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                    run_result = subprocess.run(
                        ["java", "-cp", str(codes_dir), "Main"],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,
                        text=True,  # Important for proper text handling
                        check=True
                    )
            else:
                return f"Compilation Error:\n{compile_result.stderr}"

    except subprocess.CalledProcessError as e:
        return f"Runtime Error:\n{e.stderr.decode()}"

    # Read the output
    with open(output_file_path, "r") as output_file:
        output_data = output_file.read()

    return output_data.strip()

