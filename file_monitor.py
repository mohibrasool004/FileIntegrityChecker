import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the event handler for file changes
class MonitorHandler(FileSystemEventHandler):
    def __init__(self, json_file='file_versions.json'):
        super().__init__()
        self.file_versions = {}
        self.json_file = json_file
        self.load_versions()

    def load_versions(self):
        # Load existing file versions from a JSON file
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                self.file_versions = json.load(f)

    def save_versions(self):
        # Save the current versions to a JSON file
        with open(self.json_file, 'w') as f:
            json.dump(self.file_versions, f, indent=4)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File {event.src_path} has been modified.")
            self.save_version(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            print(f"File {event.src_path} has been created.")
            self.save_version(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"File {event.src_path} has been deleted.")
            self.remove_file(event.src_path)

    def save_version(self, file_path):
        try:
            # Read the current file content
            with open(file_path, 'r') as f:
                current_content = f.read()
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                if file_path not in self.file_versions:
                    self.file_versions[file_path] = []
                
                # Get the last version of the content
                previous_version = self.file_versions[file_path][-1] if self.file_versions[file_path] else ("No previous version", "")
                
                # Append the new version with timestamp and content
                self.file_versions[file_path].append((timestamp, current_content))
                print(f"Version saved for {file_path} at {timestamp}.")
                print(f"Previous Content:\n{previous_version[1]}\n")
                
                self.save_versions()  # Save to JSON file after updating
        except Exception as e:
            print(f"Failed to read file {file_path}. Error: {e}")

    def remove_file(self, file_path):
        if file_path in self.file_versions:
            del self.file_versions[file_path]
            print(f"Removed file {file_path} from tracking.")
            self.save_versions()  # Save to JSON file after removing

    def display_file_statistics(self):
        while True:
            print("\nFile Statistics:")
            for file_path, versions in self.file_versions.items():
                print(f"  - {file_path}: {len(versions)} versions")
                for version in versions:
                    print(f"    * Timestamp: {version[0]}")
            time.sleep(60)  # Changed to 1 minute

# Function to start monitoring the specified folder
def start_monitoring(path_to_watch):
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        import threading
        stats_thread = threading.Thread(target=event_handler.display_file_statistics)
        stats_thread.start()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Define the folder to monitor
folder_to_monitor = r"C:\Users\mohib\Firewall\monitor_folder"

# Check if the folder exists, and create it if it doesn't
if not os.path.exists(folder_to_monitor):
    os.makedirs(folder_to_monitor)
    print(f"Created folder: {folder_to_monitor}")

# Start monitoring the folder
start_monitoring(folder_to_monitor)
