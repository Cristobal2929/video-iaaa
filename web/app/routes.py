from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import uuid, json, os, threading, queue
from engine.pipeline import run_pipeline
from app.database import get_db, init_db

app = Flask(__name__)
app.secret_key = "fenix_secret_2026"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACES_DIR = os.path.join(BASE_DIR, "workspaces")
init_db()
task_queue = queue.Queue()

def worker():
    while True:
        data = task_queue.get()
        conn = get_db()
        try:
            conn.execute("UPDATE jobs SET status='processing' WHERE id=?", (data['id'],))
            conn.commit()
            out = run_pipeline(data['query'], workspace_path=data['path'])
            conn.execute("UPDATE jobs SET status='completed', output=? WHERE id=?", (out, data['id']))
            conn.execute("UPDATE users SET credits=credits-1 WHERE id=?", (data['uid'],))
            conn.commit()
        except Exception as e:
            conn.execute("UPDATE jobs SET status='error', error=? WHERE id=?", (str(e), data['id']))
            conn.commit()
        finally: task_queue.task_done()

threading.Thread(target=worker, daemon=True).start()

@app.route("/")
def home():
    uid = str(uuid.uuid4())
    conn = get_db()
    conn.execute("INSERT INTO users (id, name, credits) VALUES (?, 'Admin', 999999)", (uid,))
    conn.commit()
    session["user_id"] = uid
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    uid = session.get("user_id")
    if not uid: return redirect("/")
    conn = get_db()
    u = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    p = conn.execute("SELECT * FROM projects WHERE user_id=?", (uid,)).fetchall()
    j = conn.execute("SELECT * FROM jobs WHERE user_id=? ORDER BY ROWID DESC", (uid,)).fetchall()
    return render_template("dashboard.html", user=dict(u), projects=[dict(x) for x in p], jobs=[dict(x) for x in j])

@app.route("/create_project", methods=["POST"])
def create_project():
    uid = session.get("user_id")
    pid = str(uuid.uuid4())
    name = request.form.get("name", "Nuevo Proyecto")
    conn = get_db()
    conn.execute("INSERT INTO projects (id, user_id, name, timeline) VALUES (?, ?, ?, '[]')", (pid, uid, name))
    conn.commit()
    return redirect(url_for("editor", project_id=pid))

@app.route("/editor/<project_id>")
def editor(project_id):
    uid = session.get("user_id")
    conn = get_db()
    u = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    p = conn.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone()
    return render_template("editor.html", project=dict(p), user=dict(u))

@app.route("/generate", methods=["POST"])
def generate():
    uid = session.get("user_id")
    conn = get_db()
    u = conn.execute("SELECT credits FROM users WHERE id=?", (uid,)).fetchone()
    if not u or u['credits'] <= 0: return jsonify({"status":"error", "message":"Sin créditos"}), 403
    jid = str(uuid.uuid4())
    path = os.path.join(WORKSPACES_DIR, jid)
    os.makedirs(path, exist_ok=True)
    conn.execute("INSERT INTO jobs (id, user_id, status, query) VALUES (?, ?, 'queued', ?)", (jid, uid, request.json.get("query")))
    conn.commit()
    task_queue.put({'id': jid, 'uid': uid, 'query': request.json.get("query"), 'path': path})
    return jsonify({"status": "queued", "job_id": jid})

@app.route("/status/<jid>")
def status(jid):
    conn = get_db()
    j = conn.execute("SELECT * FROM jobs WHERE id=?", (jid,)).fetchone()
    return jsonify(dict(j))

@app.route("/download/<jid>")
def download(jid):
    conn = get_db()
    j = conn.execute("SELECT * FROM jobs WHERE id=?", (jid,)).fetchone()
    return send_file(j["output"], as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
