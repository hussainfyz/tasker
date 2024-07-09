import sqlite3

def create_db():
    conn = sqlite3.connect('notifications.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        heading TEXT,
        message TEXT,
        category TEXT CHECK (category IN ('normal', 'important', 'warning', 'error', 'high_importance')),
        file_path TEXT,
        for_user TEXT
    )
    """)
    conn.commit()
    conn.close()

def fetch_recent_notifications(for_user, limit=10):
    conn = sqlite3.connect('notifications.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT heading, message, category, file_path FROM notifications 
    WHERE for_user = ? 
    ORDER BY timestamp DESC 
    LIMIT ?
    """, (for_user, limit))
    notifications = cursor.fetchall()
    conn.close()
    return notifications

def log_notification(heading, message, category, file_path, for_user="user1"):
    conn = sqlite3.connect('notifications.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (heading, message, category, file_path, for_user)
        VALUES (?, ?, ?, ?, ?)
    """, (heading, message, category, file_path, for_user))
    conn.commit()
    conn.close()

# Create the database and tables if they don't exist
#create_db()

# Insert some dummy data
#log_notification("System Update", "System update completed successfully.", "normal", "/path/to/system_update.txt")
#log_notification("Low Disk Space", "The disk space on server1 is below 10%.", "warning", "/path/to/disk_space_warning.txt")
#log_notification("High CPU Usage", "CPU usage on server2 is over 90%.", "important", "/path/to/cpu_usage.txt")
#log_notification("Service Down", "The database service is not responding.", "error", "/path/to/service_down.txt")
#log_notification("Security Alert", "Multiple failed login attempts detected.", "high_importance", "/path/to/security_alert.txt")
