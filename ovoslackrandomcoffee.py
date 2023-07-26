import os
import random
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Setup
slack_token = os.getenv("SLACK_API_TOKEN")
client = WebClient(token=slack_token)
channel_id = os.getenv("SLACK_CHANNEL_ID")


def get_channel_members(channel_id):
    try:
        response = client.conversations_members(channel=channel_id)
        members = response["members"]
        bot_user_id = client.auth_test()["user_id"]  # get the bot's user ID
        members.remove(bot_user_id)  # remove the bot from the list of members
        return members
    except SlackApiError as e:
        print(f"Error getting channel members: {e}")
        return None


def generate_pairs(members):
    if len(members) < 2:
        print("Not enough members for a pair.")
        return None

    # Randomly select two members for the pair
    pair = random.sample(members, 2)

    return [pair]


def post_pairs_to_channel(pairs, channel_id):
    for pair in pairs:
        message = f"Random coffee pair: <@{pair[0]}> and <@{pair[1]}>"
        try:
            client.chat_postMessage(channel=channel_id, text=message)
        except SlackApiError as e:
            print(f"Error posting message: {e}")


def main():
    members = get_channel_members(channel_id)
    if members is None:
        print("Failed to get channel members.")
        return
    pairs = generate_pairs(members)
    post_pairs_to_channel(pairs, channel_id)


if __name__ == "__main__":
    main()
