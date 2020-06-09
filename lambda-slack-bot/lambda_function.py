import json
import os
import hmac
import hashlib
import base64
import urllib.parse

from botocore.vendored import requests

def lambda_handler(event, context):

    yelp_api_key = os.environ["yelp_api_key"]
    headers = {'Authorization': 'Bearer {0}'.format(yelp_api_key)}
    url ='https://api.yelp.com/v3/businesses/search'

    params = {'term':'food','location':'Toronto', 'attributes':'hot_and_new'}
    req = requests.get(url, params=params, headers=headers)
    # Make sure this request has come from Slack
    if not verify_request(event):
        # If you're having problems, uncomment this line and check the cloudwatch logs:
        #print(json.dumps(event))
        return {
            'statusCode': 401
        }

    parsed = json.loads(req.text)
    businesses = parsed["businesses"]
    restaurants = []
    for business in businesses:
        restaurants.append("Name: {0}".format(business["name"]))
        restaurants.append("Yelp Rating: {0}".format(business["rating"]))
        restaurants.append("Yelp URL: {0}\n".format(business["url"]))

    listToStr = '\n'.join([str(elem) for elem in restaurants])
    # Return the response as JSON
    return {
        'body': json.dumps({
            'text': listToStr,
            'response_type': 'in_channel'
        }),
        "headers": {"Content-Type": "application/json"},
        "statusCode": 200,
    }



def verify_request(event):
    # Refer to this document for information on verifying requests:
    # https://api.slack.com/docs/verifying-requests-from-slack

    signature = event['headers']['x-slack-signature']
    request_body = base64.b64decode(event['body']).decode('ascii') if event['isBase64Encoded'] else event['body']
    req = 'v0:' + event['headers']['x-slack-request-timestamp'] + ':' + request_body
    request_hash = 'v0=' + hmac.new(
        os.environ["SIGNING_SECRET"].encode('utf-8'),
        req.encode('utf-8'), hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(request_hash, signature)
