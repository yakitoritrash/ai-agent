import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_work = os.path.abspath(working_directory)
    path = os.path.abspath(os.path.join(working_directory, file_path))
    if not (path == abs_work or path.startswith(abs_work + os.sep)):
        return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    if os.path.isdir(path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
    except Exception as e:
        return f"Error: creating directory: {e}"
    try:
        with open(path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
name="write_file",
description="Write into files in the specified file, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="The file to write content into, relative to the working directory.",
        ),
        "content": types.Schema(
            type=types.Type.STRING,
            description="The content that is written in the given file.",
        ),
    },
),
)
