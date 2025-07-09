import cv2
from deepface import DeepFace

def detect_forgery(original_image_path, suspect_image_path):
    try:
        # Compare the original and suspect images
        result = DeepFace.verify(img1_path=original_image_path, img2_path=suspect_image_path, enforce_detection=False)
        if not result["verified"]:
            print(f"[ALERT] Possible forgery detected between:\nOriginal: {original_image_path}\nSuspect: {suspect_image_path}")
        else:
            print("No forgery detected. Images match.")
    except Exception as e:
        print(f"[ERROR] Could not analyze images: {e}")

if __name__ == "__main__":
    #  usage
    original_image = "original_campaign_image.jpg"  #  original image path
    suspect_image = "sample_campaign_image.jpg"      # suspect image path
    detect_forgery(original_image, suspect_image)