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
                existing = db.query(Location).filter(Location.device_id == parsed["device_id"]).first()
                
                if not existing or parsed["timestamp"] > existing.timestamp:
                    if existing:
                        db.delete(existing)
                    db.add(Location(**parsed))
                    db.commit()
                    logging.info(f"Saved location for device {parsed['device_id']}")
                else:
                    logging.info(f"Ignored historical packet for {parsed['device_id']} (timestamp older)")
                db.close()
            else:
                logging.warning("Packet could not be parsed")
        except Exception as e:
            logging.error(f"Error handling connection: {e}")
            
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = socketserver.TCPServer(("0.0.0.0", 9000), GPSHandler)
    server.serve_forever()
        