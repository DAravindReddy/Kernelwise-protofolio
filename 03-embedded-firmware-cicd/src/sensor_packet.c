#include "sensor_packet.h"

uint16_t calculate_crc16(const uint8_t *data, size_t length) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < length; i++) {
        crc ^= (uint16_t)data[i];
        for (int b = 0; b < 8; b++) {
            if (crc & 0x0001) {
                crc = (crc >> 1) ^ 0xA001;
            } else {
                crc = crc >> 1;
            }
        }
    }
    return crc;
}

bool serialize_sensor_packet(uint16_t sensor_id, int16_t temp, uint32_t press, sensor_packet_t *pkt) {
    if (!pkt) return false;
    pkt->start_byte = PACKET_START_BYTE;
    pkt->sensor_id = sensor_id;
    pkt->temperature_raw = temp;
    pkt->pressure_raw = press;
    pkt->end_byte = PACKET_END_BYTE;

    /* Compute CRC over payload: sensor_id (2) + temp (2) + press (4) = 8 bytes */
    const uint8_t *payload = (const uint8_t *)pkt + 1;
    pkt->checksum = calculate_crc16(payload, 8);
    return true;
}

bool deserialize_and_verify_packet(const sensor_packet_t *pkt, uint16_t *sensor_id, int16_t *temp, uint32_t *press) {
    if (!pkt) return false;
    if (pkt->start_byte != PACKET_START_BYTE || pkt->end_byte != PACKET_END_BYTE) {
        return false;
    }
    const uint8_t *payload = (const uint8_t *)pkt + 1;
    uint16_t expected_crc = calculate_crc16(payload, 8);
    if (pkt->checksum != expected_crc) {
        return false;
    }
    if (sensor_id) *sensor_id = pkt->sensor_id;
    if (temp) *temp = pkt->temperature_raw;
    if (press) *press = pkt->pressure_raw;
    return true;
}
