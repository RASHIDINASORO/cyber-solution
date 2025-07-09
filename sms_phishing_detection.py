from transformers import pipeline

# (sentiment analysis)
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

def log_alert(sms_text, score, log_file="phishing_alerts.log"):
    with open(log_file, "a") as f:
        f.write(f"[ALERT] Possible phishing SMS detected:\n{sms_text}\nScore: {score}\n\n")

def check_sms_for_phishing(sms_text):
    result = classifier(sms_text)[0]
    label = result['label']
    score = result['score']
    #treat NEGATIVE as phishing, POSITIVE as safe
    if label == "NEGATIVE" and score > 0.8:
        print(f"[ALERT] Possible phishing SMS detected:\n{sms_text}\nScore: {score}\n")
        log_alert(sms_text, score)
    else:
        print(f"Checked SMS: {sms_text[:50]}...")

if __name__ == "__main__":
    # Simulated incoming SMS messages
    sms_samples = [
        "Dear voter, your NEC account is suspended. Click http://fake-link.com to reactivate.",
        "Vote for your favorite candidate by replying YES or NO.",
        "Congratulations! You have won a prize. Send your bank details to claim.",
        "Official NEC update: Polling stations open at 7am tomorrow."
    ]
    for sms in sms_samples:
        check_sms_for_phishing(sms)