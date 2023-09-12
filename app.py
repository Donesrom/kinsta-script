import time
import requests
import os

from dotenv.main import load_dotenv

load_dotenv()

WEBHOOK = os.getenv("WEBHOOK")

def get_disk_usage(path="/mnt/persistent/data"):
  # Gets the disk usage of the persistent storage disk.
  response = requests.get("https://my-kinsta-site.com/wp-json/wp/v2/stats/disk", params={"path": path})
  if response.status_code == 200:
    return response.json()
  else:
    raise Exception("Error getting disk usage")

def send_slack_alert(message):
  # Sends an alert to Slack via a webhook.
  requests.post(WEBHOOK,
                json={"text": message})

def main():
  # The main function.
  threshold = 1000
  while True:
    disk_usage = get_disk_usage()
    free_space = disk_usage["free"]
    if free_space < threshold:
      message = "Warning: Free disk space is less than {} GB".format(threshold)
      send_slack_alert(message)
      time.sleep(60)


if __name__ == "__main__":
  main()

