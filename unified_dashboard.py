import streamlit as st
import os

# Hide Streamlit's default menu and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.set_page_config(page_title=" Election Cybersecurity Dashboard", layout="wide")
st.title("Election Cybersecurity Dashboard")

tab1, tab2, tab3 = st.tabs(["Facebook misinformation", "SMS Phishing", "Image forgery"])

# --- Facebook Misinformation Tab ---
with tab1:
    st.header("Facebook misinformation alerts")
    def load_fb_alerts(log_file="misinformation_alerts.log"):
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
                        try:
                            alert["Score"] = float(line.split(":")[1].strip())
                        except ValueError:
                            alert["Score"] = line.split(":")[1].strip()
                if alert:
                    alerts.append(alert)
        except FileNotFoundError:
            st.warning(f"Log file '{log_file}' not found. No alerts to display.")
        return alerts

    fb_alerts = load_fb_alerts()
    if fb_alerts:
        st.write(f"Total alerts: {len(fb_alerts)}")
        st.table(fb_alerts)
    else:
        st.info("No Facebook misinformation alerts found.")

# --- SMS Phishing Tab ---
with tab2:
    st.header("Detected phishing SMS alerts")
    def load_sms_alerts(log_file="phishing_alerts.log"):
        try:
            with open(log_file, "r") as f:
                content = f.read()
            alerts = content.strip().split("\n\n")
            return [a for a in alerts if a]
        except FileNotFoundError:
            return []

    sms_alerts = load_sms_alerts()
    if sms_alerts:
        for alert in sms_alerts:
            st.warning(alert)
    else:
        st.success("No phishing SMS detected yet.")

    st.caption("Dashboard updates when new alerts are logged.")

# --- Image Forgery Tab ---
with tab3:
    st.header("Image forgery detection")
    st.write("Upload an original image and a suspect image to check for possible forgery.")

    try:
        from deepface import DeepFace
        import tempfile

        original_image = st.file_uploader("Upload Original Image", type=["jpg", "jpeg", "png"], key="orig")
        suspect_image = st.file_uploader("Upload Suspect Image", type=["jpg", "jpeg", "png"], key="susp")

        if original_image and suspect_image:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as orig_tmp, \
                 tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as susp_tmp:
                orig_tmp.write(original_image.read())
                susp_tmp.write(suspect_image.read())
                orig_path = orig_tmp.name
                susp_path = susp_tmp.name

            try:
                result = DeepFace.verify(img1_path=orig_path, img2_path=susp_path, enforce_detection=False)
                if not result["verified"]:
                    st.error("Possible forgery detected! The images do not match.")
                else:
                    st.success("No forgery detected. The images match.")
            except Exception as e:
                st.error(f"Error analyzing images: {e}")

            # Clean up files
            os.remove(orig_path)
            os.remove(susp_path)
        else:
            st.info("Please upload both images to proceed.")
    except ImportError:
        st.warning("DeepFace is not installed. Image forgery detection is unavailable.")
