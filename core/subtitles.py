import os

def generate_subtitles(script):
    os.makedirs("storage/output", exist_ok=True)
    lines = script.split("\n")

    srt = []
    t = 0

    for line in lines:
        if line.strip():
            srt.append(f"{t} --> {t+3}\n{line}\n")
            t += 3

    path = "storage/output/subs.srt"
    with open(path, "w") as f:
        f.write("\n".join(srt))

    return path
