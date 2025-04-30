from app.parser import parse_location_packet

# LAT = -21.01 / LON = -42.53 / SPEED = 60 / DIRECTION = 54.87
# FLAGS: D600 → gps_fixed + ignition_on + latitude- + longitude-
VALID_PACKET = "50F70A3F730000000266313672156F00000000000000000000D6003C014096500288F4D072BD73C4"

def test_latitude_longitude_are_valid_ranges():
    result = parse_location_packet(bytes.fromhex(VALID_PACKET))
    assert -90.0 <= result["latitude"] <= 90.0
    assert -180.0 <= result["longitude"] <= 180.0

def test_parser_rejects_invalid_header():
    invalid_packet = "00000A3F73025EFCF950026F017D784000008CA018003C01672D6802C8524E72BD0000"
    result = parse_location_packet(bytes.fromhex(invalid_packet))
    assert result is None

def test_parser_rejects_wrong_msg_type():
    packet = bytearray.fromhex(VALID_PACKET)
    packet[8] = 0x01
    result = parse_location_packet(bytes(packet))
    assert result is None
