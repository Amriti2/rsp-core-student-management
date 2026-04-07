import threading
import webbrowser

from app import app

def start_flask():
    """Start the Flask server in a separate thread."""
    try:
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Error starting Flask server: {e}")

if __name__ == '__main__':
    # Start the Flask server thread
    print("🚀 Starting Flask server...")
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()

    # Open the app in the default web browser
    try:
        print("🚀 Opening RSP Core in the default web browser...")
        webbrowser.open('http://127.0.0.1:5000')
    except Exception as e:
        print(f"❌ Error opening browser: {e}")

    # Keep the application running
    t.join()