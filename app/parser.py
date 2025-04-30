import struct

def parse_location_packet(data: bytes):
    if data[:2] != b'\x50\xF7' or data[-2:] != b'\x73\xC4':
        return None

    device_id = data[2:8].hex().upper()
    msg_type = data[8]

    if msg_type != 0x02:
        return None

    payload = data[9:-2]
    timestamp = struct.unpack('>I', payload[0:4])[0]
    direction = struct.unpack('>H', payload[4:6])[0] / 100.0
    speed = payload[17]
    latitude = struct.unpack('>I', payload[18:22])[0] / 1000000
    longitude = struct.unpack('>I', payload[22:26])[0] / 1000000
    flags = struct.unpack('>H', payload[16:18])[0]

    gps_fixed = bool(flags & (1 << 15))
    ignition_on = bool(flags & (1 << 13))

    return {
        "device_id": device_id,
        "timestamp": timestamp,
        "latitude": -latitude if flags & (1 << 12) else latitude,
        "longitude": -longitude if flags & (1 << 11) else longitude,
        "speed": speed,
        "direction": direction,
        "ignition_on": ignition_on,
        "gps_fixed": gps_fixed
    }