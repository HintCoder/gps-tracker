import struct
import logging

def parse_location_packet(data: bytes):
    try:
        # Valida cabeçalho e rodapé
        if data[:2] != b'\x50\xF7' or data[-2:] != b'\x73\xC4':
            logging.warning("Invalid packet header or footer")
            return None

        device_id = data[2:8].hex().upper()
        msg_type = data[8]

        # Tipo de mensagem precisa ser 0x02 (localização)
        if msg_type != 0x02:
            logging.info(f"Ignoring non-location packet from device {device_id}")
            return None

        payload = data[9:-2]

        timestamp = struct.unpack('>I', payload[0:4])[0]
        direction = struct.unpack('>H', payload[4:6])[0] / 100.0
        flags = struct.unpack('>H', payload[16:18])[0]
        speed = payload[18]
        latitude = struct.unpack('>I', payload[19:23])[0] / 1e6
        longitude = struct.unpack('>I', payload[23:27])[0] / 1e6

        gps_fixed = bool(flags & (1 << 15))
        ignition_on = bool(flags & (1 << 13))
        latitude = -latitude if flags & (1 << 12) else latitude
        longitude = -longitude if flags & (1 << 11) else longitude

        return {
            "device_id": device_id,
            "timestamp": timestamp,
            "latitude": latitude,
            "longitude": longitude,
            "speed": speed,
            "direction": direction,
            "ignition_on": ignition_on,
            "gps_fixed": gps_fixed
        }

    except Exception as e:
        logging.error(f"Error parsing packet: {e}")
        return None
