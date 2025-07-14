from flask import Flask, request, render_template_string
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Twilio credentials from .env 
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

# HTML form as a string
html_form = '''
<!DOCTYPE html>
<html>
<head>
  <title>Pill Reminder</title>
</head>
<body>
  <h2>📱 Set Your Pill Reminder</h2>
  <form method="POST">
    <label>📞 Phone Number:</label><br>
    <input type="text" name="phone" placeholder="+91XXXXXXXXXX" required><br><br>

    <label>💊 Reminder Message:</label><br>
    <textarea name="message" placeholder="Take your Vitamin D at 8 PM" required></textarea><br><br>

    <button type="submit">Send Reminder</button>
  </form>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        phone_number = request.form["phone"]
        message_body = request.form["message"]

        try:
            message = client.messages.create(
                body=message_body,
                from_=twilio_phone,
                to=phone_number
            )
            print(f" Message sent to {phone_number}. SID: {message.sid}")
            return f" Message sent! SID: {message.sid}"
        except Exception as e:
            print(f" Error sending message to {phone_number}: {e}")
            return " Failed to send message. Please try again later."

    return render_template_string(html_form)

if __name__ == "__main__":
    app.run(debug=True)
