#include "ring_buffer.h"

void ring_buffer_init(ring_buffer_t *rb) {
    if (!rb) return;
    rb->head = 0;
    rb->tail = 0;
    rb->count = 0;
}

bool ring_buffer_push(ring_buffer_t *rb, uint8_t byte) {
    if (!rb || ring_buffer_is_full(rb)) {
        return false;
    }
    rb->buffer[rb->head] = byte;
    rb->head = (rb->head + 1) % RING_BUFFER_SIZE;
    rb->count++;
    return true;
}

bool ring_buffer_pop(ring_buffer_t *rb, uint8_t *byte) {
    if (!rb || !byte || ring_buffer_is_empty(rb)) {
        return false;
    }
    *byte = rb->buffer[rb->tail];
    rb->tail = (rb->tail + 1) % RING_BUFFER_SIZE;
    rb->count--;
    return true;
}

size_t ring_buffer_available(const ring_buffer_t *rb) {
    return rb ? rb->count : 0;
}

bool ring_buffer_is_full(const ring_buffer_t *rb) {
    return rb ? (rb->count >= RING_BUFFER_SIZE) : true;
}

bool ring_buffer_is_empty(const ring_buffer_t *rb) {
    return rb ? (rb->count == 0) : true;
}
