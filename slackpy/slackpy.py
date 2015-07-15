#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Takahiro Ikeuchi'
# Minor changes to formatting and message defaults for my own preferences

import os
import requests
import json
import traceback
from argparse import ArgumentParser


class Messenger:
    def __init__(self, web_hook_url, channel=None, username=None):

        self.web_hook_url = web_hook_url
        self.channel = channel
        self.username = username
        if channel is None\
           or channel.startswith('#')\
           or channel.startswith('@'):
            pass

        else:
            raise ValueError('channel must be started with "#" or "@".')

    def __build_payload(self, message, title, color):

        __fields = {
            "title": title,
            "text": message,
            "color": color,
            "fallback": title,
        }

        __attachments = {
            "fields": __fields
        }

        payload = {
            "attachments": __attachments
        }
        # Optional channel and username, if not specified the integration
        # defaults are used
        if self.channel is not None:
            payload["channel"] = self.channel
        if self.username is not None:
            payload["username"] = self.username,

        return payload

    def __send_notification(self, message, title, color='good'):
        """Send a message to a channel.
        Args:
            title: The message title.
            message: The message body.
            color: Can either be one of 'good', 'warning', 'danger',
                   or any hex color code

        Returns:
            api_response:

        Raises:
            TODO:
        """
        payload = self.__build_payload(message, title, color)

        try:
            response = requests.post(self.web_hook_url,
                                     data=json.dumps(payload))

        except Exception:
            raise Exception(traceback.format_exc())

        else:
            if response.status_code == 200:
                return response

            else:
                raise Exception(response.content.decode())

    def debug(self, message, title):
        return self.__send_notification(message=message,
                                        title=title,
                                        color='#03A9F4')

    def info(self, message, title):
        return self.__send_notification(message=message,
                                        title=title,
                                        color='good')

    def warning(self, message, title):
        return self.__send_notification(message=message,
                                        title=title,
                                        color='warning')

    def error(self, message, title):
        return self.__send_notification(message=message,
                                        title=title,
                                        color='danger')


def main():
    try:
        web_hook_url = os.environ["SLACK_INCOMING_WEB_HOOK"]

    except KeyError:
        print('ERROR: Please set the SLACK_INCOMING_WEB_HOOK variable in your'
              'environment.')

    else:
        parser = ArgumentParser(description='slackpy command line tool')
        parser.add_argument('-m', '--message', type=str, required=True,
                            help='Message')
        parser.add_argument('-t', '--title', type=str, required=True,
                            help='Title')
        parser.add_argument('-c', '--channel', required=False,
                            help='Channel', default=None)
        parser.add_argument('-n', '--name', type=str, required=False,
                            help='Name of Sender', default=None)

        levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        parser.add_argument('-l', '--level', default='INFO', choices=levels)

        args = parser.parse_args()

        client = Messenger(web_hook_url, args.channel, args.name)

        if args.level == "DEBUG":
            response = client.debug(args.message, args.title)

        elif args.level == "INFO":
            response = client.info(args.message, args.title)

        elif args.level == "WARNING":
            response = client.warning(args.message, args.title)

        elif args.level == "ERROR":
            response = client.error(args.message, args.title)

        else:
            raise Exception("'Level' must be selected from among: "
                            + ", ".join(levels))

        if response.status_code == 200:
            print(True)

        else:
            print(False)

if __name__ == "__main__":
    main()
