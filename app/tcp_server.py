import socketserver
from .parser import parse_location_packet
from .database import SessionLocal
from .models import Location

class GPSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        parsed = parse_location_packet(data)
        
        if parsed:
            db = SessionLocal()
            #TODO: fazer com update
            db.query(Location).filter(Location.device_id == parsed["device_id"]).delete()
            db.add(Location(**parsed))
            db.commit()
            db.close()
        else:
            print("Invalid packet received")
            
        
if __name__ == "__main__":
    server = socketserver.TCPServer(("0.0.0.0", 9000), GPSHandler)
    server.serve_forever()
        