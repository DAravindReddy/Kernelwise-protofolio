"""
Matter Smart Device Edge Gateway Daemon
Coordinates virtual and physical bridged smart devices, commissioning, and state synchronization.
"""

from typing import Dict, List, Optional
from src.matter_model import (
    ClusterId,
    MatterEndpoint,
    create_dimmable_light_endpoint,
    create_door_lock_endpoint,
    create_temperature_sensor_endpoint,
)


class MatterGatewayDaemon:
    def __init__(self):
        self.endpoints: Dict[int, MatterEndpoint] = {}
        self.commissioning_state = "IDLE"
        self._init_default_smart_home()

    def _init_default_smart_home(self):
        # Endpoint 1: Living Room Smart Light
        self.endpoints[1] = create_dimmable_light_endpoint(endpoint_id=1, on=True, level=180)
        # Endpoint 2: Indoor Climate Sensor
        self.endpoints[2] = create_temperature_sensor_endpoint(endpoint_id=2, temp_c=24.2)
        # Endpoint 3: Front Entry Smart Lock
        self.endpoints[3] = create_door_lock_endpoint(endpoint_id=3, locked=True)

    def get_all_endpoints(self) -> List[Dict]:
        return [ep.to_dict() for ep in self.endpoints.values()]

    def execute_command(self, endpoint_id: int, cluster_name: str, command: str, params: Optional[Dict] = None) -> Dict:
        if endpoint_id not in self.endpoints:
            return {"success": False, "error": f"Endpoint {endpoint_id} not found"}

        ep = self.endpoints[endpoint_id]
        params = params or {}

        # 1. OnOff Cluster Commands
        if cluster_name.lower() in ["onoff", "0x0006"]:
            cluster = ep.clusters.get(ClusterId.ON_OFF)
            if not cluster:
                return {"success": False, "error": "Endpoint does not support OnOff cluster"}
            if command.lower() == "toggle":
                curr = cluster.get_attr("on_off")
                cluster.set_attr("on_off", not curr)
            elif command.lower() == "on":
                cluster.set_attr("on_off", True)
            elif command.lower() == "off":
                cluster.set_attr("on_off", False)
            return {"success": True, "endpoint_id": endpoint_id, "state": cluster.get_attr("on_off")}

        # 2. LevelControl Cluster Commands
        elif cluster_name.lower() in ["levelcontrol", "0x0008"]:
            cluster = ep.clusters.get(ClusterId.LEVEL_CONTROL)
            if not cluster:
                return {"success": False, "error": "Endpoint does not support LevelControl"}
            lvl = int(params.get("level", 254))
            lvl = max(0, min(254, lvl))
            cluster.set_attr("current_level", lvl)
            return {"success": True, "endpoint_id": endpoint_id, "current_level": lvl}

        # 3. DoorLock Cluster Commands
        elif cluster_name.lower() in ["doorlock", "0x0101"]:
            cluster = ep.clusters.get(ClusterId.DOOR_LOCK)
            if not cluster:
                return {"success": False, "error": "Endpoint does not support DoorLock"}
            if command.lower() == "lock":
                cluster.set_attr("lock_state", 1)  # 1 = Locked
            elif command.lower() == "unlock":
                cluster.set_attr("lock_state", 2)  # 2 = Unlocked
            return {"success": True, "endpoint_id": endpoint_id, "lock_state": cluster.get_attr("lock_state")}

        # 4. Temperature Measurement Update
        elif cluster_name.lower() in ["temperaturemeasurement", "0x0402"]:
            cluster = ep.clusters.get(ClusterId.TEMPERATURE_MEASUREMENT)
            if not cluster:
                return {"success": False, "error": "Endpoint does not support TemperatureMeasurement"}
            val = float(params.get("temp_c", 22.0))
            cluster.set_attr("measured_value", int(val * 100))
            return {"success": True, "endpoint_id": endpoint_id, "temp_c": val}

        return {"success": False, "error": f"Unknown cluster {cluster_name} or command {command}"}

    def commission_new_device(self, device_type: str, name: str) -> Dict:
        new_id = max(self.endpoints.keys(), default=0) + 1
        if device_type.lower() == "light":
            ep = create_dimmable_light_endpoint(new_id, on=True, level=254)
        elif device_type.lower() == "sensor":
            ep = create_temperature_sensor_endpoint(new_id, temp_c=22.0)
        elif device_type.lower() == "lock":
            ep = create_door_lock_endpoint(new_id, locked=True)
        else:
            return {"success": False, "error": f"Unsupported device type: {device_type}"}

        self.endpoints[new_id] = ep
        return {"success": True, "endpoint_id": new_id, "device_type": device_type, "status": "COMMISSIONED"}
