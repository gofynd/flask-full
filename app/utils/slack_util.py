from app import slack_client


class SlackUtil:

    def list_channels(self):
        channels_call = slack_client.api_call("channels.list")
        if channels_call.get('ok'):
            return channels_call['channels']
        return None

    def channel_info(self, channel_id):
        channel_info = slack_client.api_call("channels.info", channel=channel_id)
        if channel_info:
            return channel_info['channel']
        return None

    def send_message(self, channel_id, message, username='icon_emoji', icon_emoji=':robot_face:'):
        slack_client.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=message,
            username=username,
            icon_emoji=icon_emoji)
