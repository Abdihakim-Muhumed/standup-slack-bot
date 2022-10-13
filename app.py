from lib2to3.pgen2 import token
import os
from webbrowser import get

from slack_bolt import App


app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("app_home_opened")
def update_home_tab_with_introduction(client,event,logger):
    try:
        client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to _Stand up Bot_* :tada:"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Hi, my name is Stand up Bot. I am a friendly bot and i will be in charge of the daily stand ups in this workspace."
                        }
                    }
                ]
            }
        )
    except Exception as e:
            logger.error(f"Error publishing home tab introduction: {e}")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
