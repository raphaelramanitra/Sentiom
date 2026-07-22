from typing import Dict, Any, List

DEFAULT_THRESHOLDS = {
    "temp_critical_c": 2.0, #A-001
    "temp_high_c": 7.0,  #A-002
    "leak_resistance_critical_ohm": 100000, #A-003
    "battery_medium_pct": 15, #A-004
    "heartbeat_status_high": "OK", #A-005
    "water_flow_high_lpm": 20.0, #A-006
    "signal_quality_high_dbm": -85, #A-007 

}

def detect_anomalies(device_type: str, values: Dict[str, Any], thresholds: Dict[str, Any] = None) -> List[Dict[str, str]]:
    """
    Analyzes telemetry values and returns a list of detected anomalies.
    """
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    anomalies = []

    def _add(rule_id: str, severity: str, desc: str):
        anomalies.append({"rule_id": rule_id, "severity": severity, "description": desc})

    #A-001 & A-002: Temperature anomalies
    temp = values.get("temperature_c")
    if temp is not None:
        if temp < thresholds["temp_critical_c"]:
            _add("A-002", "Critical", f"Temperature below {thresholds['temp_critical_c']} °C")
        elif temp < thresholds["temp_high_c"]:
            _add("A-002", "High", f"Temperature below {thresholds['temp_high_c']} °C")

    #A-003: Leak resistance anomaly
    leak_resistance = values.get("leak_resistance_ohm")
    if leak_resistance is not None and leak_resistance < thresholds["leak_resistance_critical_ohm"]:
        _add("A-003", "Critical", f"Leak resistance below {thresholds['leak_resistance_critical_ohm']} ohms")
    
    #A-004: Battery level anomaly
    battery_level = values.get("battery_pct")
    if battery_level is not None and battery_level < thresholds["battery_medium_pct"]:
        _add("A-004", "Medium", f"Battery level below {thresholds['battery_medium_pct']}%")
    
    #A-005: Heartbeat status anomaly
    if device_type == "galileo":
        heartbeat_status = values.get("heartbeat")
        if heartbeat_status is not None and heartbeat_status != thresholds["heartbeat_status_high"]:
            _add("A-005", "High", f"Heartbeat is '{heartbeat_status}' instead of '{thresholds['heartbeat_status_high']}'")
    
    #A-006: Water flow anomaly
    hot_flow = values.get("hot_flow_lpm", 0)
    cold_flow = values.get("cold_flow_lpm", 0)
    if hot_flow > thresholds["water_flow_high_lpm"] or cold_flow > thresholds["water_flow_high_lpm"]:
        _add("A-006", "High", f"Water flow exceeds {thresholds['water_flow_high_lpm']} LPM")
    
    #A-007: Signal quality anomaly
    signal_quality = values.get("signal_quality")
    if signal_quality is not None and signal_quality < thresholds["signal_quality_high_dbm"]:
        _add("A-007", "High", f"Signal quality below {thresholds['signal_quality_high_dbm']} dBm")

    return anomalies