import os

def generate_voice(text):
    os.makedirs("storage/output", exist_ok=True)
    path = "storage/output/voice.txt"
    with open(path, "w") as f:
        f.write(text)
    return path
