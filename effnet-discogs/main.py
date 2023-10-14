from fastapi import FastAPI, File, UploadFile
import subprocess
import shlex


app = FastAPI()

@app.post("/predict/")
async def predict(audio: UploadFile):
    # Save the audio file to a temporary location
    temp_audio_path = f"/tmp/{audio.filename}"
    with open(temp_audio_path, "wb") as audio_file:
        audio_file.write(audio.file.read())

    # Cog 
    cog_command = f"cog predict -i audio=@{temp_audio_path}"
    process = subprocess.Popen(shlex.split(cog_command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Cog returns a JSON string
    if process.returncode == 0:
        return {"result": stdout.decode("utf-8")}
    else:
        return {"error": stderr.decode("utf-8")}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
