#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "../src/ring_buffer.h"
#include "../src/sensor_packet.h"

static int tests_run = 0;
static int tests_passed = 0;

#define TEST_ASSERT(cond, msg) do { \
    tests_run++; \
    if (cond) { \
        tests_passed++; \
    } else { \
        printf("[FAIL] Line %d: %s\n", __LINE__, msg); \
    } \
} while(0)

void test_ring_buffer_basic(void) {
    ring_buffer_t rb;
    ring_buffer_init(&rb);

    TEST_ASSERT(ring_buffer_is_empty(&rb) == true, "Buffer should be empty upon init");
    TEST_ASSERT(ring_buffer_available(&rb) == 0, "Buffer count should be 0");

    bool pushed = ring_buffer_push(&rb, 0x42);
    TEST_ASSERT(pushed == true, "Push should succeed");
    TEST_ASSERT(ring_buffer_available(&rb) == 1, "Buffer count should be 1");
    TEST_ASSERT(ring_buffer_is_empty(&rb) == false, "Buffer should not be empty");

    uint8_t val = 0;
    bool popped = ring_buffer_pop(&rb, &val);
    TEST_ASSERT(popped == true, "Pop should succeed");
    TEST_ASSERT(val == 0x42, "Popped value should match 0x42");
    TEST_ASSERT(ring_buffer_is_empty(&rb) == true, "Buffer should be empty after pop");
}

void test_sensor_packet_crc(void) {
    sensor_packet_t pkt;
    bool serialized = serialize_sensor_packet(0x101, 255, 101325, &pkt);
    TEST_ASSERT(serialized == true, "Serialization should succeed");
    TEST_ASSERT(pkt.start_byte == PACKET_START_BYTE, "Start byte must match 0xAA");
    TEST_ASSERT(pkt.end_byte == PACKET_END_BYTE, "End byte must match 0x55");

    uint16_t s_id = 0;
    int16_t temp = 0;
    uint32_t press = 0;
    bool valid = deserialize_and_verify_packet(&pkt, &s_id, &temp, &press);
    TEST_ASSERT(valid == true, "Packet validation must succeed");
    TEST_ASSERT(s_id == 0x101, "Sensor ID should match 0x101");
    TEST_ASSERT(temp == 255, "Temperature should match 255");
    TEST_ASSERT(press == 101325, "Pressure should match 101325");

    /* Test corrupted checksum */
    pkt.checksum ^= 0x00FF;
    bool corrupted = deserialize_and_verify_packet(&pkt, &s_id, &temp, &press);
    TEST_ASSERT(corrupted == false, "Corrupted packet must fail CRC verification");
}

int main(void) {
    printf("========================================================\n");
    printf("   KERNELWISE LABS // FIRMWARE UNIT TEST SUITE (C99)    \n");
    printf("========================================================\n");
    test_ring_buffer_basic();
    test_sensor_packet_crc();
    printf("--------------------------------------------------------\n");
    printf(" Tests Run: %d | Passed: %d | Failed: %d\n", tests_run, tests_passed, tests_run - tests_passed);
    printf("========================================================\n");
    return (tests_run == tests_passed) ? 0 : 1;
}
