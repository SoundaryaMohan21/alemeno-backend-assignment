import json
import time
import google.generativeai as genai

# -------------------------------
# Gemini API Key
# -------------------------------
import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-1.5-flash")


# --------------------------------------------------
# Fill missing transaction categories
# --------------------------------------------------
def classify_transactions(transactions):

    prompt = f"""
You are a finance expert.

Classify each transaction into ONE category only.

Possible Categories:

Food
Shopping
Travel
Transport
Utilities
Cash Withdrawal
Entertainment
Other

Return ONLY a JSON array.

Transactions:

{json.dumps(transactions, indent=2)}
"""

    for _ in range(3):

        try:

            response = model.generate_content(prompt)

            text = response.text.strip()

            text = (
                text.replace("```json", "")
                    .replace("```", "")
                    .strip()
            )

            return json.loads(text)

        except Exception:

            time.sleep(2)

    return None


# --------------------------------------------------
# Detect Anomaly
# --------------------------------------------------
def detect_anomaly(transaction):

    prompt = f"""
You are a fraud detection assistant.

Transaction:

{json.dumps(transaction, indent=2)}

Reply ONLY with:

Yes

or

No
"""

    try:

        response = model.generate_content(prompt)

        ans = response.text.strip().lower()

        if "yes" in ans:
            return "Yes"

        return "No"

    except Exception:

        return "No"


# --------------------------------------------------
# Generate Spending Summary
# --------------------------------------------------
def generate_summary(summary_data):

    prompt = f"""
You are a financial analyst.

Analyse the spending.

Return ONLY JSON.

Format:

{{
    "narrative":"",
    "risk_level":"Low"
}}

Data:

{json.dumps(summary_data, indent=2)}
"""

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        text = (
            text.replace("```json", "")
                .replace("```", "")
                .strip()
        )

        return json.loads(text)

    except Exception:

        return {
            "narrative": "Summary generation failed.",
            "risk_level": "Unknown"
        }