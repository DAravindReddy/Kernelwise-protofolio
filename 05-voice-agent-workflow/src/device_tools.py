"""
Device Diagnostics, Warranty, and RMA Scheduling Tools for Voice Agent
"""

import datetime
from typing import Dict


MOCK_WARRANTY_DB = {
    "SN-88210": {"status": "ACTIVE", "tier": "Platinum Enterprise", "expires": "2027-12-31"},
    "SN-55420": {"status": "ACTIVE", "tier": "Standard Consumer", "expires": "2026-11-15"},
    "SN-10044": {"status": "EXPIRED", "tier": "Standard Consumer", "expires": "2024-05-01"},
}

MOCK_DIAGNOSTIC_DB = {
    "SN-88210": {"soc_temp_c": 64.2, "battery_health_pct": 78, "active_errors": ["ERR_THERMAL_THROTTLE_ZONE2"]},
    "SN-55420": {"soc_temp_c": 38.5, "battery_health_pct": 98, "active_errors": []},
    "SN-10044": {"soc_temp_c": 42.0, "battery_health_pct": 65, "active_errors": ["ERR_BATTERY_DEGRADED"]},
}


def check_warranty(serial_number: str) -> Dict:
    sn_clean = serial_number.strip().upper()
    if sn_clean in MOCK_WARRANTY_DB:
        record = MOCK_WARRANTY_DB[sn_clean]
        return {"success": True, "serial": sn_clean, "status": record["status"], "tier": record["tier"], "expires": record["expires"]}
    return {"success": True, "serial": sn_clean, "status": "ACTIVE", "tier": "Standard Warranty", "expires": "2027-01-01"}


def trigger_remote_diagnostics(serial_number: str) -> Dict:
    sn_clean = serial_number.strip().upper()
    data = MOCK_DIAGNOSTIC_DB.get(sn_clean, {"soc_temp_c": 45.0, "battery_health_pct": 92, "active_errors": []})
    return {
        "success": True,
        "serial": sn_clean,
        "temperature_c": data["soc_temp_c"],
        "battery_health": data["battery_health_pct"],
        "errors": data["active_errors"],
    }


def schedule_rma_repair(serial_number: str, issue_description: str, preferred_time: str) -> Dict:
    now = datetime.datetime.now()
    ticket_id = f"RMA-{now.strftime('%y%m%d')}-{abs(hash(serial_number)) % 10000:04d}"
    return {
        "success": True,
        "ticket_id": ticket_id,
        "serial": serial_number.strip().upper(),
        "scheduled_slot": preferred_time,
        "assigned_engineer": "Senior Hardware Field Tech (Kernelwise Labs)",
        "confirmation_message": f"Appointment booked under ticket {ticket_id} for {preferred_time}.",
    }
