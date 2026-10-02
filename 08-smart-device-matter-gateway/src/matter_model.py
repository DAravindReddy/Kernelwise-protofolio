"""
Matter Data Model Abstraction (Endpoints, Clusters, Attributes, and Commands)
Compliant with CSA Matter 1.2 Core Specification concepts.
"""

from dataclasses import asdict, dataclass, field
from enum import IntEnum
from typing import Any, Dict, List, Optional


class ClusterId(IntEnum):
    DESCRIPTOR = 0x001D
    ON_OFF = 0x0006
    LEVEL_CONTROL = 0x0008
    TEMPERATURE_MEASUREMENT = 0x0402
    DOOR_LOCK = 0x0101


@dataclass
class MatterAttribute:
    id: int
    name: str
    type_name: str
    value: Any


@dataclass
class MatterCluster:
    cluster_id: int
    name: str
    attributes: Dict[str, MatterAttribute] = field(default_factory=dict)

    def get_attr(self, name: str) -> Any:
        return self.attributes[name].value if name in self.attributes else None

    def set_attr(self, name: str, val: Any):
        if name in self.attributes:
            self.attributes[name].value = val


@dataclass
class MatterEndpoint:
    endpoint_id: int
    device_type_name: str
    device_type_id: int
    clusters: Dict[int, MatterCluster] = field(default_factory=dict)

    def add_cluster(self, cluster: MatterCluster):
        self.clusters[cluster.cluster_id] = cluster

    def to_dict(self):
        return {
            "endpoint_id": self.endpoint_id,
            "device_type": self.device_type_name,
            "clusters": {
                c.name: {attr_name: attr.value for attr_name, attr in c.attributes.items()}
                for c in self.clusters.values()
            },
        }


def create_dimmable_light_endpoint(endpoint_id: int, on: bool = True, level: int = 200) -> MatterEndpoint:
    ep = MatterEndpoint(endpoint_id, "Dimmable Light", 0x0101)
    # OnOff Cluster
    on_off = MatterCluster(ClusterId.ON_OFF, "OnOff")
    on_off.attributes["on_off"] = MatterAttribute(0x0000, "OnOff", "bool", on)
    ep.add_cluster(on_off)
    # LevelControl Cluster
    lvl = MatterCluster(ClusterId.LEVEL_CONTROL, "LevelControl")
    lvl.attributes["current_level"] = MatterAttribute(0x0000, "CurrentLevel", "u8", level)
    ep.add_cluster(lvl)
    return ep


def create_temperature_sensor_endpoint(endpoint_id: int, temp_c: float = 23.5) -> MatterEndpoint:
    ep = MatterEndpoint(endpoint_id, "Temperature Sensor", 0x0302)
    temp = MatterCluster(ClusterId.TEMPERATURE_MEASUREMENT, "TemperatureMeasurement")
    # Matter temp is stored in 0.01 deg C increments (s16)
    temp.attributes["measured_value"] = MatterAttribute(0x0000, "MeasuredValue", "s16", int(temp_c * 100))
    ep.add_cluster(temp)
    return ep


def create_door_lock_endpoint(endpoint_id: int, locked: bool = True) -> MatterEndpoint:
    ep = MatterEndpoint(endpoint_id, "Door Lock", 0x000A)
    lock = MatterCluster(ClusterId.DOOR_LOCK, "DoorLock")
    # LockState: 1 = Locked, 2 = Unlocked
    lock.attributes["lock_state"] = MatterAttribute(0x0000, "LockState", "enum8", 1 if locked else 2)
    ep.add_cluster(lock)
    return ep
