from http import client
from lib2to3.pgen2 import token
import os
from webbrowser import get

from slack_bolt import App
from slack_sdk.errors import SlackApiError

import schedule
from schedule import every, repeat, run_pending
import time

from blocks import BLOCK_STANDUP_MESSAGE, BLOCK_HOME_INTRO

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("app_home_opened")
def home_tab_introduction(client,event,logger):
    try:
        client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "blocks": BLOCK_HOME_INTRO
            }
        )
    except Exception as e:
            logger.error(f"Error publishing home tab introduction: {e}")

@repeat(every().monday.at("18:00"))
@repeat(every().tuesday.at("18:00"))
@repeat(every().wednesday.at("18:00"))
@repeat(every().thursday.at("18:00"))
def alert_before_sending_standups(client=app.client):   
    try:
        result = client.chat_postMessage(
            channel="#all-students",
            text="Good evening everyone! It is Stand up time, I am sending out standups in 5 minutes time. "
        )
        return(result)

    except SlackApiError as e:
        return(f"Error: {e}")
    
@repeat(every().monday.at("18:06"))
@repeat(every().tuesday.at("18:06"))
@repeat(every().wednesday.at("18:06"))
@repeat(every().thursday.at("18:06"))
def alert_after_sending_standups(client=app.client):   
    try:
        result = client.chat_postMessage(
            channel="#all-students",
            text="Good evening once more! I have sent out standups to everyone. Please take time to do your standups! "
        )
        return(result)

    except SlackApiError as e:
        return(f"Error: {e}")

@repeat(every().monday.at("18:05"))
@repeat(every().tuesday.at("18:05"))
@repeat(every().wednesday.at("18:05"))
@repeat(every().thursday.at("18:05"))
def send_stand_up(client=app.client,):
    members = get_members(client=app.client)
    TMs = []
    for member in members:
        if member not in TMs:
            client.chat_postMessage(
                channel=member,
                blocks=BLOCK_STANDUP_MESSAGE
            )

def get_members(client=app.client):
    conversations = client.conversations_list()
    members = []
    for channel in conversations['channels']:
        if channel["name"]=="all-students":
            members = client.conversations_members(channel=channel["id"])["members"]
    return members 
       
while app:
    schedule.run_pending()
    time.sleep(1)
    
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
