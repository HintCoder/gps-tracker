import socketserver
import logging
from .parser import parse_location_packet
from .database import SessionLocal
from .models import Location

class GPSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            data = self.request.recv(1024)
            parsed = parse_location_packet(data)
            
            if parsed:
                db = SessionLocal()
                #TODO: fazer com update
                db.query(Location).filter(Location.device_id == parsed["device_id"]).delete()
                db.add(Location(**parsed))
                db.commit()
                db.close()
                logging.info(f"Saved location for device {parsed['device_id']}")
            else:
                logging.warning("Packet could not be parsed")
        except Exception as e:
            logging.error(f"Error handling connection: {e}")
            
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = socketserver.TCPServer(("0.0.0.0", 9000), GPSHandler)
    server.serve_forever()
        