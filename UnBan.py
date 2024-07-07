#unbanbot shitcoded by sysR@M
TOKEN = "YOUR_USER_TOKEN"
SERVER_ID = "SERVER_ID_TO_UNBAN_MEMBERS"
exceptreason = ["Spam", "Malware"]
import time
import requests

print("Getting ban entries...")
resp = requests.get(f"https://discord.com/api/v9/guilds/{SERVER_ID}/bans", headers={
    "Authorization": f"{TOKEN}",
})
if resp.status_code == 401:
    print("Unauthorized Failed!")
    exit()
elif resp.status_code == 403:
    print("Permissions denied")
    exit()
elif resp.status_code == 400:
    print("Bad Request")
    exit()
elif resp.status_code != 200:
    print(f"An unknown error occurred! {resp.status_code}: {resp.text}")
    exit()
else:
    try:
        ban_entries = resp.json()
    except Exception as e:
        print("Failed to decode ban entries: {e}")
        exit()
    else:
        print(f"Successfully got {len(ban_entries)} ban entries!")

for index, ban_entry in enumerate(ban_entries):
    user_id = ban_entry["user"]["id"]
    username = ban_entry["user"]["username"]
    banreason = ban_entry["reason"]
    
    if banreason is None:
        print(f"Skipping user {username} ({user_id}) because ban reason is not specified.")
        continue
    
    found_exception = False
    for exceptreason_ in exceptreason:
        if exceptreason_ in banreason:
            found_exception = True
            break
    
    if found_exception:
        continue
    
    resp = requests.delete(f"https://discord.com/api/v9/guilds/{SERVER_ID}/bans/{user_id}", headers={
        "Authorization": f"{TOKEN}",
    })
    if resp.status_code == 204:
        print(f"Successfully unbanned username: {username} userid: {user_id} banreason: {banreason}!")
    else:
        print(f"Failed to unban username: {username} userid: {user_id}! {resp.status_code}: {resp.text}")
    
    if int(resp.headers.get("X-RateLimit-Remaining", 0)) < 1:
        RateLimit = float(resp.headers.get("X-RateLimit-Reset-After", 1))
        RateLimit_Remaining = float(resp.headers.get("X-RateLimit-Remaining", 0))
        print(f"Waiting {RateLimit} seconds for ratelimit to reset... | Request Remaining: {RateLimit_Remaining} | Remaining bans: {len(ban_entries) - (index + 1)}")
        time.sleep(RateLimit)

print("Done!")
