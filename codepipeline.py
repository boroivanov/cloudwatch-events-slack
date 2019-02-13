import os
import json

from slackclient import SlackClient


slack_token = os.environ["SLACK_API_TOKEN"]
channel = os.environ['SLACK_CHANNEL']
excluded_stages = os.environ.get('EXCLUDED_STAGES', '').split(',')
excluded_successes = os.environ.get('EXCLUDED_SUCCESSES', '').split(',')


def lambda_handler(event, context):
    # For debugging so you can see raw event format.
    print('Here is the event:')
    print(json.dumps(event))

    if event['source'] != 'aws.codepipeline':
        raise ValueError('Function only supports input from events with'
                         'a source type of: aws.codepipeline')

    sc = SlackClient(slack_token)

    details = event['detail']

    # Don't notify on the following
    if details['stage'] in excluded_stages:
        print('Skipping Slack notification for {}'.format(details['stage']))
        return
    if details['stage'] in excluded_successes \
            and details['state'] == 'SUCCEEDED':
        print('Skipping Slack notification for {} {}'.format(
            details['stage'], details['state']))
        return

    # Map Slack colors to states
    if details['state'] in ['FAILED', 'CANCELED']:
        color = 'danger'
    elif details['state'] in ['SUCCEEDED', 'RESUMED']:
        color = 'good'
    else:
        color = 'warning'

    params = {
        'channel': channel,
        'attachments': [
            {
                'color': color,
                'text': '{} {} {}'.format(details['pipeline'],
                                          details['stage'],
                                          details['state'])
            }
        ]
    }
    response = sc.api_call('chat.postMessage', **params)
    print(response)


if __name__ == '__main__':
    event = {
        'source': 'aws.codepipeline',
        'detail': {
            'pipeline': 'test-pipeline',
            'stage': 'stage',
            'state': 'FAILED'
        }
    }
    lambda_handler(event, None)
