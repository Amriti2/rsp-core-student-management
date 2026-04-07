import socket
import webbrowser

from app import app


def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    local_ip = get_local_ip()

    print("Starting RSP Core for network access...")
    print(f"This laptop: http://127.0.0.1:{port}")
    print(f"Same Wi-Fi/LAN: http://{local_ip}:{port}")

    try:
        webbrowser.open(f"http://127.0.0.1:{port}")
    except Exception as error:
        print(f"Could not open browser automatically: {error}")

    app.run(host=host, port=port, debug=False, use_reloader=False)