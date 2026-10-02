# Project 08: Architecture Specification — Smart Device Matter Gateway

## 1. System Block Diagram

```mermaid
flowchart TD
    subgraph Ecosystem Integrations
        AH[Apple Home / Google Home / Alexa] --- B[Matter IPv6 Thread / Wi-Fi Network]
        HA[Home Assistant / Local LAN] --- REST[Gateway REST API]
    end

    subgraph Kernelwise Edge Gateway Daemon
        B <--> PROTO[Matter Protocol Abstraction Layer]
        REST <--> DISPATCH[Gateway Command Dispatcher]
        
        PROTO --- REG[Local Device Registry & Endpoints]
        DISPATCH --- REG
        
        REG --> EP1[Endpoint 1: Smart Dimmable Light]
        REG --> EP2[Endpoint 2: Environmental Sensor]
        REG --> EP3[Endpoint 3: Motorized Smart Lock]
    end

    subgraph Physical / Bridged Smart Devices
        EP1 <-->|BLE / Zigbee Bridge| D1[BLE Smart Bulb]
        EP2 <-->|I2C Local Sensor| D2[BMP280 Sensor]
        EP3 <-->|RS-485 / Relays| D3[Electronic Strike Lock]
    end

    subgraph Presentation & Control
        DISPATCH <--> UI[Web Management Console: Port 8084]
    end
```

---

## 2. Matter Data Model Cluster Mappings

| Endpoint | Device Type | Cluster ID | Cluster Name | Attributes | Supported Commands |
|---|---|---|---|---|---|
| **0** | Root Node (0x0016) | `0x001D` | Descriptor | DeviceTypeList, ServerList | Query Descriptor |
| **1** | Dimmable Light (0x0101) | `0x0006` | On/Off | `OnOff: bool` | On, Off, Toggle |
| **1** | Dimmable Light (0x0101) | `0x0008` | Level Control | `CurrentLevel: 0-254` | MoveToLevel |
| **2** | Temp Sensor (0x0302) | `0x0402` | Temperature Measurement | `MeasuredValue: s16` | Read Temperature |
| **3** | Door Lock (0x000A) | `0x0101` | Door Lock | `LockState: 1=Locked, 2=Unlocked` | LockDoor, UnlockDoor |
