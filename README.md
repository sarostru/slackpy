# slackpy

slackpy is [Slack][] client library for specific logging.

## Install

To get the original one,
```sh
pip install slackpy
```
To install this fork, 
```sh
pip install git+https://github.com/sarostru/slackpy.git#egg=slackpy
```

## Dependencies

-   requests 2.7

## Sample Code

```python
import slackpy

INCOMING_WEB_HOOK = 'your_web_hook_url'
CHANNEL = '#general'
USER_NAME = 'Logger'

# Create a new instance.
logging = slackpy.SlackLogger(INCOMING_WEB_HOOK, CHANNEL, USER_NAME)
# CHANNEL and USER_NAME may both by None in which case the default
# values for the webhook are used

# LogLevel: DEBUG
logging.debug(message='Your Message', title="DEBUG Notification")

# LogLevel: INFO
logging.info(message='Your Message', title="INFO Notification")

# LogLevel: WARNING
logging.warning(message='Your Message', title="WARNING Notification")

# LogLevel: ERROR
logging.error(message='Your Message', title="ERROR Notification")
```

### Correspondence table

Method | LogLevel | Color
:----: | :------: | :----:
debug() | DEBUG | #03A9F4 (Light Blue)
info() | INFO | good (green)
warn() | WARNING | warning (orange)
error() | ERROR | danger (red)

## Command line

```sh
export SLACK_INCOMING_WEB_HOOK='your_web_hook_url'

# LogLevel: DEBUG
slackpy -c '#your_channel' -t 'DEBUG' -m 'Message' -l 'DEBUG'

# LogLevel: INFO
slackpy -c '#your_channel' -t 'INFO' -m 'Message' -l 'INFO'

# LogLevel: WARNING
slackpy -c '#your_channel' -t 'WARNING' -m 'Message' -l 'WARNING'

# LogLevel: ERROR
slackpy -c '#your_channel' -t 'ERROR' -m 'Message' -l 'ERROR'

```

  [Slack]: https://slack.com
