from fastapi import FastAPI, Request
import subprocess, tempfile, os, base64, glob, shutil, logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

def find_first_mp4(root_dir: str):
    # walk and return first .mp4 found
    for dirpath, _, files in os.walk(root_dir):
        for f in files:
            if f.lower().endswith(".mp4"):
                return os.path.join(dirpath, f)
    # fallback: glob search
    matches = glob.glob(os.path.join(root_dir, "**", "*.mp4"), recursive=True)
    return matches[0] if matches else None

@app.get("/health")
async def health():
    return {"ok": True, "msg": "manim-runner healthy"}

@app.post("/run")
async def run_manim(request: Request):
    """
    Accepts JSON: { "code": "<python manim code as string>" }
    Returns: { success: bool, video_base64: str } on success
    """
    data = await request.json()
    code = data.get("code", "")
    if not code:
        return {"success": False, "error": "No code provided"}

    with tempfile.TemporaryDirectory() as tmp:
        # write the code to a file
        scene_file = os.path.join(tmp, "scene.py")
        with open(scene_file, "w") as f:
            f.write(code)

        # run manim to render all scenes in the file at medium quality
        try:
            # run manim; render all scenes in the file
            subprocess.run(["manim", "-q", "m", scene_file], check=True, cwd=tmp, timeout=300)
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": f"manim failed: {e}"}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "manim render timed out"}

        # find the produced mp4 file
        mp4_path = find_first_mp4(tmp)
        if not mp4_path or not os.path.exists(mp4_path):
            # try the typical media folder in case manim used a different cwd
            media_loc = os.path.join(tmp, "media")
            mp4_path = find_first_mp4(media_loc) if os.path.exists(media_loc) else None

        if not mp4_path:
            # As a last resort, copy media from default working dir if present
            possible_media = os.path.join(os.getcwd(), "media")
            mp4_path = find_first_mp4(possible_media) if os.path.exists(possible_media) else None

        if not mp4_path:
            return {"success": False, "error": "No output MP4 found after rendering"}

        with open(mp4_path, "rb") as fh:
            encoded = base64.b64encode(fh.read()).decode()

        # optional: include filename and size
        stat = os.stat(mp4_path)
        return {"success": True, "video_base64": encoded, "filename": os.path.basename(mp4_path), "size_bytes": stat.st_size}
