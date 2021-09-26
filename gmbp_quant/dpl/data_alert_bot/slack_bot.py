import slack
import datetime
import gmbp_quant.env_config as ecfg

"""
Dependencies: slack (from PyPI)
              Include SLACK_BOT_TOKEN in env_config.py and env_config.cfg
"""

def text_bot(msg='nothing to report', channel_name='#youtube-python-slack-bot'):
    client = slack.WebClient(token=ecfg.get_env_config().get(ecfg.Prop.SLACK_BOT_TOKEN))

    client.chat_postMessage(channel=channel_name,
                            text=msg)


if __name__ == '__main__':

    forms = ['4', '13F', '13FHA']
    try:
        text_bot(forms[0])

    except:
        now = datetime.datetime.now()
        msg = '[' + now.strftime("%Y-%m-%d %H:%M:%S") + ']' + \
              ' Some error has occurred.'
        text_bot(msg=msg)
