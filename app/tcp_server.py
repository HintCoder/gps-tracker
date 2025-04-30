import socketserver

class GPSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        print(f"Received data: {data.hex()}")
        
if __name__ == "__main__":
    server = socketserver.TCPServer(("0.0.0.0", 9000), GPSHandler)
    server.serve_forever()
        