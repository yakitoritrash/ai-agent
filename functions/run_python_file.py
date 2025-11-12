import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_work = os.path.abspath(working_directory)
    path = os.path.abspath(os.path.join(working_directory, file_path))
    if not (path == abs_work or path.startswith(abs_work + os.sep)):
        return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.exists(path):
        return (f'Error: File "{file_path}" not found.')
    if not path.endswith(".py"):
        return (f'Error: "{file_path}" is not a Python file.')
    try:
        cmd_list = ["python", file_path, *args]
        completed_process = subprocess.run(cmd_list, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=abs_work)
        stdEr = completed_process.stderr
        stdOu = completed_process.stdout
        if stdEr == "" and stdOu == "":
            return f"No output produced."
        x = f"STDOUT: {stdOu}\nSTDERR: {stdEr}"
        if completed_process.returncode != 0:
            x = x + f"\nProcess exited with code {completed_process.returncode}"
        return x
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
schema_run_python_file = types.FunctionDeclaration(
name="run_python_file",
description="Run the python file from the specified file, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="The file that is to run, relative to the working directory."
        ),
        "args": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(type=types.Type.STRING),
            description="A list of string arguments to pass to the python script."
            )
    },
    required=["file_path"]
),
)
