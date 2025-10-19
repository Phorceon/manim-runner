from fastapi import FastAPI, Request
import subprocess, tempfile, os, base64

app = FastAPI()

@app.post("/run")
async def run_manim(request: Request):
    data = await request.json()
    code = data.get("code", "")
    if not code:
        return {"success": False, "error": "No code provided"}

    with tempfile.TemporaryDirectory() as tmp:
        file_path = os.path.join(tmp, "scene.py")
        with open(file_path, "w") as f:
            f.write(code)

        try:
            subprocess.run(["manim", file_path, "-qm", "-o", "result.mp4"], check=True)

            output_path = None
            for root, _, files in os.walk(tmp):
                if "result.mp4" in files:
                    output_path = os.path.join(root, "result.mp4")
                    break
            if not output_path:
                return {"success": False, "error": "No video produced"}

            with open(output_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            return {"success": True, "video_base64": encoded}

        except subprocess.CalledProcessError as e:
            return {"success": False, "error": str(e)}
