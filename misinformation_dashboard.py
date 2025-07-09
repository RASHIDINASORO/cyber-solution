import streamlit as st

st.title("Social Media Misinformation Detection Dashboard")

log_file = "misinformation_alerts.log"

def load_alerts(log_file):
    try:
        with open(log_file, "r") as f:
            content = f.read()
        alerts = content.strip().split("\n\n")
        return [a for a in alerts if a]
    except FileNotFoundError:
        return []

alerts = load_alerts(log_file)

st.header("Detected Misinformation Alerts")
if alerts:
    for alert in alerts:
        st.warning(alert)
else:
    st.success("No misinformation detected yet.")

st.caption("Dashboard updates when new alerts are logged.")