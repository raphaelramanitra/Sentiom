from services.anomaly_engine import detect_anomalies

def test_no_anomalies():
    # Test case where no anomalies are detected
    values = {
        "temperature_c": 21.0,
        "battery_pct": 85,
        "leak_resistance_ohm": 150000,
        "signal_quality": -60,
    }
    anomalies = detect_anomalies("kepler", values)

    #Expecting empty list
    assert len(anomalies) == 0

def test_critical_temperature_a002():
    # Test case for critical temperature anomaly (A-002)

    values = {"temperature_c": 1.5}  #under the critical threshold of 2.0 °C
    anomalies = detect_anomalies("kepler", values)
    
    assert len(anomalies) == 1
    assert anomalies[0]["rule_id"] == "A-002"
    # Verify that
    assert anomalies[0]["severity"] == "Critical"

def test_multiple_anomalies_simultaneously():
    # Verify that the engine can detect multiple errors at the same time
    values = {
        "temperature_c": 1.5,           # A-002
        "leak_resistance_ohm": 50000,   # A-003
        "battery_pct": 10               # A-004
    }
    anomalies = detect_anomalies("kepler", values)
    
    assert len(anomalies) == 3
    
    # Extract just the rule IDs for easy validation
    rule_ids = [a["rule_id"] for a in anomalies]
    assert "A-002" in rule_ids
    assert "A-003" in rule_ids
    assert "A-004" in rule_ids