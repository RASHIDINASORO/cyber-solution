import streamlit as st
from deepface import DeepFace
import tempfile
import os

st.title("Image Forgery Detection Dashboard")

st.write("Upload an original image and a suspect image to check for possible forgery.")

original_image = st.file_uploader("Upload Original Image", type=["jpg", "jpeg", "png"])
suspect_image = st.file_uploader("Upload Suspect Image", type=["jpg", "jpeg", "png"])

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

    # Clean up temp files
    os.remove(orig_path)
    os.remove(susp_path)
else:
    st.info("Please upload both images to proceed.")