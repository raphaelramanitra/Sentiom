SUPPORTED_DEVICES = {
    "kepler": {
        "temperature_c": float,
        "humidity_pct": float,
        "leak_resistance_ohm": (int, float),
        "battery_pct": int,
        "signal_quality": int
    },
    "archimede": {
        "valve_state": str,
        "flow_hot_lmin": float,
        "flow_cold_lmin": float
    },
    "newton": {
        "motion_detected": bool,
        "luminosity_lux": (int, float),
        "temperature_c": float
    },
    "galileo": {
        "heartbeat": str,
        "cpu_usage_pct": float,
        "disk_free_gb": (int, float),
        "service_status": str
    },
    "thermostat": {
        "setpoint_c": float,
        "room_temperature_c": float,
        "heating_active": bool
    }
}