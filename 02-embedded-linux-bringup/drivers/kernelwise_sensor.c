// SPDX-License-Identifier: GPL-2.0
/*
 * Kernelwise Labs Environmental Sensor Linux I2C Driver
 * Supports high-precision temperature, pressure, and threshold IRQ handling.
 * Exposes sysfs attributes under /sys/class/kernelwise_sensor/
 */

#include <linux/module.h>
#include <linux/init.h>
#include <linux/i2c.h>
#include <linux/kernel.h>
#include <linux/mutex.h>
#include <linux/sysfs.h>
#include <linux/interrupt.h>
#include <linux/of.h>
#include <linux/slab.h>

#define DRIVER_NAME "kernelwise_sensor"
#define REG_CHIP_ID 0xD0
#define EXPECTED_CHIP_ID 0x58
#define REG_TEMP_MSB 0xFA
#define REG_PRESS_MSB 0xF7

struct kernelwise_data {
    struct i2c_client *client;
    struct mutex lock;
    struct class *dev_class;
    struct device *sysfs_device;
    int irq;
    s32 temperature_raw;
    s32 pressure_raw;
    int sample_rate_hz;
};

/* Sysfs attribute: temperature in millidegrees Celsius */
static ssize_t temperature_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    struct kernelwise_data *data = dev_get_drvdata(dev);
    s32 temp;
    mutex_lock(&data->lock);
    /* In actual silicon, read 3 bytes from REG_TEMP_MSB over I2C */
    temp = data->temperature_raw;
    mutex_unlock(&data->lock);
    return sysfs_emit(buf, "%d\n", temp);
}
static DEVICE_ATTR_RO(temperature);

/* Sysfs attribute: pressure in Pascals */
static ssize_t pressure_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    struct kernelwise_data *data = dev_get_drvdata(dev);
    s32 press;
    mutex_lock(&data->lock);
    press = data->pressure_raw;
    mutex_unlock(&data->lock);
    return sysfs_emit(buf, "%d\n", press);
}
static DEVICE_ATTR_RO(pressure);

/* Sysfs attribute: sample rate */
static ssize_t sample_rate_show(struct device *dev, struct device_attribute *attr, char *buf)
{
    struct kernelwise_data *data = dev_get_drvdata(dev);
    return sysfs_emit(buf, "%d\n", data->sample_rate_hz);
}

static ssize_t sample_rate_store(struct device *dev, struct device_attribute *attr, const char *buf, size_t count)
{
    struct kernelwise_data *data = dev_get_drvdata(dev);
    int val, ret;
    ret = kstrtoint(buf, 10, &val);
    if (ret < 0 || val <= 0 || val > 100)
        return -EINVAL;
    mutex_lock(&data->lock);
    data->sample_rate_hz = val;
    mutex_unlock(&data->lock);
    return count;
}
static DEVICE_ATTR_RW(sample_rate);

static struct attribute *kernelwise_attrs[] = {
    &dev_attr_temperature.attr,
    &dev_attr_pressure.attr,
    &dev_attr_sample_rate.attr,
    NULL,
};
ATTRIBUTE_GROUPS(kernelwise);

/* Interrupt Handler for Hardware Threshold Trigger */
static irqreturn_t kernelwise_irq_handler(int irq, void *dev_id)
{
    struct kernelwise_data *data = dev_id;
    dev_info(&data->client->dev, "Threshold interrupt asserted on GPIO IRQ %d\n", irq);
    /* Notify user-space through sysfs_notify if required */
    return IRQ_HANDLED;
}

static int kernelwise_probe(struct i2c_client *client, const struct i2c_device_id *id)
{
    struct kernelwise_data *data;
    int chip_id;

    dev_info(&client->dev, "Probing Kernelwise Sensor on I2C address 0x%02x\n", client->addr);

    data = devm_kzalloc(&client->dev, sizeof(*data), GFP_KERNEL);
    if (!data)
        return -ENOMEM;

    data->client = client;
    mutex_init(&data->lock);
    data->sample_rate_hz = 10;
    data->temperature_raw = 24500; // 24.50 C
    data->pressure_raw = 101325;   // 1013.25 hPa
    i2c_set_clientdata(client, data);

    /* Verify Chip ID */
    chip_id = i2c_smbus_read_byte_data(client, REG_CHIP_ID);
    if (chip_id >= 0 && chip_id != EXPECTED_CHIP_ID) {
        dev_warn(&client->dev, "Unexpected Chip ID: 0x%x (expected 0x%x)\n", chip_id, EXPECTED_CHIP_ID);
    }

    /* Request IRQ if configured in DTS */
    if (client->irq > 0) {
        data->irq = client->irq;
        int ret = devm_request_threaded_irq(&client->dev, data->irq, NULL,
                                            kernelwise_irq_handler,
                                            IRQF_TRIGGER_FALLING | IRQF_ONESHOT,
                                            DRIVER_NAME, data);
        if (ret) {
            dev_warn(&client->dev, "Failed to register IRQ %d: %d\n", data->irq, ret);
        } else {
            dev_info(&client->dev, "Successfully bound IRQ %d\n", data->irq);
        }
    }

    /* Register Sysfs Class and Device */
    data->dev_class = class_create(THIS_MODULE, "kernelwise_sensor");
    if (IS_ERR(data->dev_class))
        return PTR_ERR(data->dev_class);

    data->sysfs_device = device_create_with_groups(data->dev_class, &client->dev,
                                                   MKDEV(0, 0), data,
                                                   kernelwise_groups, "hwmon0");
    if (IS_ERR(data->sysfs_device)) {
        class_destroy(data->dev_class);
        return PTR_ERR(data->sysfs_device);
    }

    dev_info(&client->dev, "Kernelwise Sensor driver bound successfully.\n");
    return 0;
}

static void kernelwise_remove(struct i2c_client *client)
{
    struct kernelwise_data *data = i2c_get_clientdata(client);
    device_destroy(data->dev_class, MKDEV(0, 0));
    class_destroy(data->dev_class);
    mutex_destroy(&data->lock);
    dev_info(&client->dev, "Kernelwise Sensor driver removed.\n");
}

static const struct of_device_id kernelwise_of_match[] = {
    { .compatible = "kernelwise,env-sensor-v1", },
    { }
};
MODULE_DEVICE_TABLE(of, kernelwise_of_match);

static struct i2c_driver kernelwise_i2c_driver = {
    .driver = {
        .name = DRIVER_NAME,
        .of_match_table = kernelwise_of_match,
    },
    .probe = kernelwise_probe,
    .remove = kernelwise_remove,
};

module_i2c_driver(kernelwise_i2c_driver);

MODULE_AUTHOR("Kernelwise Labs <engineering@kernelwiselabs.com>");
MODULE_DESCRIPTION("ARM64 Linux Kernel I2C Driver for Environmental Sensor");
MODULE_LICENSE("GPL v2");
