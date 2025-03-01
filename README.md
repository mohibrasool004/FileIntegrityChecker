File Integrity Checker with Real-Time Monitoring and Dashboard
Overview
This project is a File Integrity Checker that continuously monitors a specified folder for unauthorized file modifications, creations, or deletions. It leverages real-time file monitoring using Python's watchdog library and provides a web-based dashboard built with Flask and Flask-SocketIO. The system tracks file changes by storing file versions in a JSON file and displays live analytics on the number of changes. Additionally, it offers backup and restore capabilities via API endpoints.

Motivation
In today’s cybersecurity landscape, ensuring the integrity of critical files is paramount. Traditional file integrity monitoring systems typically perform periodic checks or rely on log-based reviews, which can delay detection of unauthorized changes. This project addresses those challenges by:

Monitoring files in real time: Immediate detection of changes.
Tracking detailed file version history: Keeping an audit trail of what changed and when.
Providing a user-friendly dashboard: A visual, web-based interface for real-time updates and analytics.
Enabling backup and restore: Safeguarding historical data for recovery and audit purposes.
Unique Features
Real-Time File Monitoring with WebSockets:
The system uses Flask-SocketIO to push live updates about file changes directly to a web dashboard—ensuring instant alerts without page refreshes.

Automated File Versioning:
Every change is logged with a timestamp and the new content is stored in a JSON file, enabling a detailed version history for audit and rollback.

Interactive Web-Based Dashboard:
A user-friendly interface allows users to select a folder and immediately begin monitoring, view live updates of file changes, and see real-time analytics (modification, creation, and deletion counts).

Backup and Restore Functionality:
Dedicated API endpoints allow users to back up the current file version data and restore from these backups, ensuring data is never lost.

Enhanced Analytics:
The dashboard provides live statistics on file activity, offering insights into the overall integrity and usage patterns of monitored directories.

Technologies Used
Python 3.13+
Flask – Web framework for building the backend.
Flask-SocketIO – For real-time communication between server and client.
watchdog – For monitoring file system events.
JSON – Used to store file version data persistently.
HTML, CSS, JavaScript – For building the interactive web dashboard.
Installation
Prerequisites
Python 3.13 or higher
pip package manager