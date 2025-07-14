import schedule
import time
from datetime import datetime

from database import get_all_reminders
from Remainder import send_sms

def check_and_send():
    now = datetime.now().strftime("%H:%M")  # Get current time (HH:MM)
    reminders = get_all_reminders()

    for r in reminders:
        # Compare current time to each reminder's scheduled time
        if r["time"] == now:
            message = f"💊 Reminder: Take your medicine {r['name']} - {r['dose']} now!"
            send_sms(r["phone"], message)
            print(f"Sent reminder to {r['phone']} for {r['name']} at {now}")

# Check every minute
schedule.every(1).minutes.do(check_and_send)

while True:
    schedule.run_pending()
    time.sleep(1)
