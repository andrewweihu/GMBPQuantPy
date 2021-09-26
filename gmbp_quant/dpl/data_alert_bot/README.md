# Data Alert Bot
A data availability check utility, checking the last data available date on the database, and post results on the Slack channel.

## To Run
```python
python data_availability_bot.py
```

## To Add Forms
Add forms, days for alert in forms_to_check.yml

Currently all forms are set to days = -1, meaning everything is reported.

## To Call Bot
slack_bot.text_bot is a callable function, can be included to post any message on the Slack channel.
