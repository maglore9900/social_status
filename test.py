import requests

# Request URL
url = "https://ioc.exchange/api/v1/statuses"

# Request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 1rSRqd5lH8a-eMpaffirG4XbZQ1OwIJiIr1GNmvpCA8",  # Replace with your actual token
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Referer": "https://ioc.exchange/home",
    "Origin": "https://ioc.exchange",
    "X-CSRF-Token": "mbJ0hBf4-rN9Vc86J7TZ--skHhgOxS1q-2amkSMqBTvpIVhWAQ-_RJUlq9n8boHlxKxrC5D7BvAFA88TMGxbHA",
}

# Payload
payload = {
    "status": "what color is the sky?",
    "in_reply_to_id": None,
    "media_ids": [],
    "sensitive": False,
    "spoiler_text": "",
    "visibility": "public",
    "poll": None,
    "language": "en"
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Print the response
if response.status_code == 200:
    print("Post successful!")
    print("Response:", response.json())
else:
    print(f"Failed to post. Status code: {response.status_code}")
    print("Response:", response.text)
