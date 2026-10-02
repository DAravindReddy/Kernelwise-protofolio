SUMMARY = "Kernelwise Labs Environmental Sensor Out-of-Tree Kernel Module"
DESCRIPTION = "Linux I2C client driver for environmental sensors with sysfs and IRQ handling"
HOMEPAGE = "https://github.com/KernelwiseLabs/embedded-linux-bringup"
LICENSE = "GPL-2.0-only"
LIC_FILES_CHKSUM = "file://COPYING;md5=b234ee4d69f5fce4486a80fdaf4a4263"

inherit module

SRC_URI = " \
    file://Makefile \
    file://kernelwise_sensor.c \
    file://COPYING \
"

S = "${WORKDIR}"

RPROVIDES:${PN} += "kernel-module-kernelwise-sensor"
AUTOLOAD += "kernelwise_sensor"
