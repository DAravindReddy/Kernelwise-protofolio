#ifndef SENSOR_PACKET_H
#define SENSOR_PACKET_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#define PACKET_START_BYTE 0xAA
#define PACKET_END_BYTE   0x55

#pragma pack(push, 1)
typedef struct {
    uint8_t start_byte;
    uint16_t sensor_id;
    int16_t temperature_raw;
    uint32_t pressure_raw;
    uint16_t checksum;
    uint8_t end_byte;
} sensor_packet_t;
#pragma pack(pop)

uint16_t calculate_crc16(const uint8_t *data, size_t length);
bool serialize_sensor_packet(uint16_t sensor_id, int16_t temp, uint32_t press, sensor_packet_t *pkt);
bool deserialize_and_verify_packet(const sensor_packet_t *pkt, uint16_t *sensor_id, int16_t *temp, uint32_t *press);

#endif /* SENSOR_PACKET_H */
