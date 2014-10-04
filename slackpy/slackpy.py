#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Takahiro Ikeuchi'

import os
import requests
import json
from argparse import ArgumentParser


class SlackLogger:
    def __init__(self, auth_token, channel, username):

        self.base_uri = 'https://slack.com/api/chat.postMessage'
        self.auth_token = auth_token
        self.channel = channel
        self.username = username

    def __send_notification(self, title, message, color='good'):
        """Send a message to a channel.
        Args:
            title: The message title.
            message: The message body.
            color: Can either be one of 'good', 'warning', 'danger', or any hex color code

        Returns:
            api_response:

        Raises:
            TODO:
        """
        __fields = {
            "title": title,
            "text": message,
            "color": color,
            "fallback": title,
        }

        __attachments = {
            "fields": __fields
        }

        params = {
            "token": self.auth_token,
            "channel": self.channel,
            "username": self.username,
            "parse": "full",
            "attachments": json.dumps(__attachments)
        }

        response = requests.post(self.base_uri, data=params)

        return response

    def info(self, title, message):

        title = 'INFO : {0}'.format(title)
        return self.__send_notification(title=title, message=message, color='good')

    def warn(self, title, message):

        title = 'WARN : {0}'.format(title)
        return self.__send_notification(title=title, message=message, color='warning')

    def error(self, title, message):

        title = 'ERROR : {0}'.format(title)
        return self.__send_notification(title=title, message=message, color='danger')


def main():
    try:
        auth_token = os.environ["SLACK_TOKEN"]

    except KeyError:
        print('ERROR: Please set the SLACK_TOKEN variable in your environment.')

    else:
        parser = ArgumentParser(description='slackpy command line tool')
        parser.add_argument('-c', '--channel', required=True, help='Channel')
        parser.add_argument('-t', '--title', type=str, required=False, help='Title')
        parser.add_argument('-m', '--message', type=str, required=True, help='Message')
        parser.add_argument('-l', '--level', type=int, default=1, choices=[1, 2, 3])

        args = parser.parse_args()

        client = SlackLogger(auth_token, args.channel, 'Logger')

        if args.level == 1:
            response = client.info(args.title, args.message)

        if args.level == 2:
            response = client.warn(args.title, args.message)

        if args.level == 3:
            response = client.error(args.title, args.message)

        if response.status_code == 200:
            print(True)

        else:
            print(False)

