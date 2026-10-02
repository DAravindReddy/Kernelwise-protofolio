cmake_minimum_required(VERSION 3.16)
project(KernelwiseFirmware C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

include_directories(src)

# Library target
add_library(firmware_core STATIC
    src/ring_buffer.c
    src/sensor_packet.c
)

# Test executable
add_executable(test_suite
    tests/test_firmware.c
)

target_link_libraries(test_suite PRIVATE firmware_core)

enable_testing()
add_test(NAME FirmwareCoreTests COMMAND test_suite)
