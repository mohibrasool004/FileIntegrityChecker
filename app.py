import os
import time
import json
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
socketio = SocketIO(app)

# To store file versions and analytics
file_versions = {}
analytics = {
    "modification_count": 0,
    "created_count": 0,
    "deleted_count": 0
}

# Event handler for monitoring files
class MonitorHandler(FileSystemEventHandler):
    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        self.load_versions()

    def load_versions(self):
        global file_versions
        if os.path.exists("file_versions.json"):
            with open("file_versions.json", "r") as f:
                file_versions = json.load(f)

    def save_versions(self):
        with open("file_versions.json", "w") as f:
            json.dump(file_versions, f, indent=4)

    def on_modified(self, event):
        if not event.is_directory:
            global analytics
            analytics["modification_count"] += 1
            self.save_version(event.src_path, "modified")

    def on_created(self, event):
        if not event.is_directory:
            global analytics
            analytics["created_count"] += 1
            self.save_version(event.src_path, "created")

    def on_deleted(self, event):
        if not event.is_directory:
            global analytics
            analytics["deleted_count"] += 1
            self.remove_file(event.src_path)

    def save_version(self, file_path, action):
        try:
            with open(file_path, 'r') as f:
                current_content = f.read()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                if file_path not in file_versions:
                    file_versions[file_path] = []

                
                file_versions[file_path].append({"timestamp": timestamp, "content": current_content, "action": action})

                self.save_versions()
                socketio.emit('file_update', {
    'file': file_path, 
    'current': f" {current_content}",  # Updated line
    'timestamp': timestamp, 
    'action': action
})
        except Exception as e:
            print(f"Failed to read file {file_path}. Error: {e}")

    def remove_file(self, file_path):
        if file_path in file_versions:
            del file_versions[file_path]
            self.save_versions()

# Function to start monitoring a folder
def start_monitoring(path_to_watch):
    event_handler = MonitorHandler(path_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# API route to start monitoring
@app.route("/start_monitoring", methods=["POST"])
def start_monitoring_route():
    folder_to_monitor = request.json.get('folder')
    if folder_to_monitor:
        start_monitoring(folder_to_monitor)
        return jsonify({"status": "Monitoring started"}), 200
    return jsonify({"status": "Folder not provided"}), 400

# API route to get file versions
@app.route("/file_versions", methods=["GET"])
def get_file_versions():
    return jsonify(file_versions), 200

# API route to get analytics
@app.route("/analytics", methods=["GET"])
def get_analytics():
    return jsonify(analytics), 200

# Route to serve the dashboard page
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)
