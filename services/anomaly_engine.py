from typing import Dict, Any, List

DEFAULT_THRESHOLDS = {
    "temp_warning_high_c": 2.0,  #A-002
    "temp_warning_critical_c": 7.0, #A-001
    "leak_resistance_critical_ohm": 100000, #A-003
    "battery_medium_pct": 15, #A-004
    "heartbeat_status_high": "OK", #A-005
    "water_flow_high_lpm": 20.0, #A-006
    "signal_quality_high_dbm": -85, #A-007 

}

def detect_anomalies(device_type: str, values: Dict[str, Any], thresholds: Dict[str, Any] = None) -> List[Dict[str, str]]:
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    anomalies = []

    #A-001 & A-002: Temperature anomalies
    temp = values.get("temperature_c")
    if temp is not None:
        if temp < thresholds["temp_warning_high_c"]:
            anomalies.append({"rule_id": "A-002", "severity": "Critical", "description": "Temperature below 2 °C"})
        elif temp < thresholds["temp_warning_critical_c"]:
            anomalies.append({"rule_id": "A-001", "severity": "High", "description": "Temperature below 7 °C"})

    #A-003: Leak resistance anomaly
    leak_resistance = values.get("leak_resistance_ohm")
    if leak_resistance is not None and leak_resistance < thresholds["leak_resistance_critical_ohm"]:
        anomalies.append({"rule_id": "A-003", "severity": "Critical", "description": "Leak resistance below threshold"})
    
    #A-004: Battery level anomaly
    battery_level = values.get("battery_pct")
    if battery_level is not None and battery_level < thresholds["battery_medium_pct"]:
        anomalies.append({"rule_id": "A-004", "severity": "Medium", "description": f"Battery level below {thresholds['battery_medium_pct']}%"})
    
    #A-005: Heartbeat status anomaly
    if device_type == "galileo":
        heartbeat_status = values.get("heartbeat")
        if heartbeat_status is not None and heartbeat_status != thresholds["heartbeat_status_high"]:
            anomalies.append({"rule_id": "A-005", "severity": "High", "description": "Heartbeat is missing or deprecated"})
    
    #A-006: Water flow anomaly
    hot_flow = values.get("hot_flow_lpm", 0)
    cold_flow = values.get("cold_flow_lpm", 0)
    if hot_flow > thresholds["water_flow_high_lpm"] or cold_flow > thresholds["water_flow_high_lpm"]:
        anomalies.append({"rule_id": "A-006", "severity": "High", "description": "Water flow exceeds threshold"})
    
    #A-007: Signal quality anomaly
    signal_quality = values.get("signal_quality")
    if signal_quality is not None and signal_quality < thresholds["signal_quality_high_dbm"]:
        anomalies.append({"rule_id": "A-007", "severity": "High", "description": "Signal quality below threshold"})
        
    return anomalies