import requests
from transformers import pipeline

# Facebook Page ID and Access Token
PAGE_ID = "Facebook_PAGE_ID"
ACCESS_TOKEN = "Facebook_PAGE_ACCESS_TOKEN"

#(sentiment analysis)
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english", framework="pt")

def log_alert(text, score, log_file="misinformation_alerts.log"):
    with open(log_file, "a") as f:
        f.write(f"[ALERT] Possible misinformation detected:\n{text}\nScore: {score}\n\n")

def fetch_facebook_posts(page_id, access_token, limit=10):
    url = f"https://graph.facebook.com/v18.0/{page_id}/posts"
    params = {
        "access_token": access_token,
        "limit": limit,
        "fields": "message,created_time"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("data", [])

if __name__ == "__main__":
    posts = fetch_facebook_posts(PAGE_ID, ACCESS_TOKEN)
    for post in posts:
        text = post.get("message", "")
        if not text:
            continue
        result = classifier(text)[0]
        label = result['label']
        score = result['score']
        if label == "NEGATIVE" and score > 0.8:
            print(f"[ALERT] Possible misinformation detected:\n{text}\nScore: {score}\n")
            log_alert(text, score)
        else:
            print(f"Checked: {text[:50]}...")