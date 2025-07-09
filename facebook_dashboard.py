import streamlit as st

st.title("Facebook Misinformation Alerts Dashboard")

def load_alerts(log_file="misinformation_alerts.log"):
    alerts = []
    try:
        with open(log_file, "r") as f:
            alert = {}
            for line in f:
                if line.startswith("[ALERT]"):
                    if alert:
                        alerts.append(alert)
                        alert = {}
                if "Possible misinformation detected:" in line:
                    alert["Message"] = line.split("detected:")[1].strip()
                elif "Score:" in line:
                    alert["Score"] = float(line.split(":")[1].strip())
            if alert:
                alerts.append(alert)
    except FileNotFoundError:
        st.warning(f"Log file '{log_file}' not found. No alerts to display.")
    return alerts

alerts = load_alerts()

if alerts:
    st.write(f"Total alerts: {len(alerts)}")
    st.table(alerts)
else:
    st.info("No alerts found.")