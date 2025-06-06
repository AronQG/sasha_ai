import subprocess
import os

BLENDER_PATH = r"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"
OUTPUT_PATH = os.path.abspath("output.png")  # Сохраняем файл в рабочей папке

def run_blender_script(script_code, output_path=OUTPUT_PATH):
    script_file = "blender_job.py"
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(script_code.replace("output.png", output_path.replace("\\", "/")))
    result = subprocess.run([
        BLENDER_PATH, "--background", "--python", script_file
    ])
    if os.path.exists(output_path):
        return output_path
    return None
