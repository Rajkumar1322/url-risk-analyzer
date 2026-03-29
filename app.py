import requests
from flask import Flask, render_template, request
import re

app = Flask(__name__)

def extract_features(url):
    features = []
    url_lower = url.lower()

    # 1. HTTPS
    features.append(1 if not url.startswith("https") else 0)

    # 2. Long URL
    features.append(1 if len(url) > 50 else 0)

    # 3. @ symbol
    features.append(1 if "@" in url else 0)

    # 4. Too many dots
    features.append(1 if url.count('.') > 3 else 0)

    # 5. IP address
    pattern = r'http[s]?://\d+\.\d+\.\d+\.\d+'
    features.append(1 if re.match(pattern, url) else 0)

    # 6. Suspicious keywords
    suspicious_words = ["login", "secure", "update", "verify", "bank", "account"]
    features.append(1 if any(word in url_lower for word in suspicious_words) else 0)

    return features


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        if not url.startswith("http"):
            return render_template("index.html", url=url, status="Invalid URL ⚠️", prob=0)

        # 🔥 Fetch Website Title (FIXED POSITION)
        page_title = "Not Available"
        try:
            response = requests.get(url, timeout=3)
            html = response.text

            if "<title>" in html:
                page_title = html.split("<title>")[1].split("</title>")[0]
        except:
            page_title = "Could not fetch"

        features = extract_features(url)

        # 🔥 Risk Scoring
        risk_score = 0
        if features[0]: risk_score += 10
        if features[1]: risk_score += 15
        if features[2]: risk_score += 25
        if features[3]: risk_score += 10
        if features[4]: risk_score += 20
        if features[5]: risk_score += 20

        risk_percent = min(risk_score, 100)

        # 🔥 STATUS LOGIC
        if risk_percent <= 35:
            status = "Safe ✅"
        elif risk_percent <= 60:
            status = "Suspicious ⚠️"
        elif risk_percent <= 80:
            status = "Risky 🚨"
        else:
            status = "Phishing ❌"

        # Reasons
        reasons = []
        if features[0]: reasons.append("No HTTPS (Not Secure)")
        if features[1]: reasons.append("URL is too long")
        if features[2]: reasons.append("Contains '@' symbol")
        if features[3]: reasons.append("Too many dots in URL")
        if features[4]: reasons.append("Uses IP address")
        if features[5]: reasons.append("Suspicious keywords detected")

        return render_template("index.html",
                               url=url,
                               status=status,
                               prob=risk_percent,
                               reasons=reasons,
                               title=page_title)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)