import json
import time

import requests
from elasticapm import capture_serverless, capture_span, get_client
from elasticapm.metrics.base_metrics import MetricSet


@capture_serverless()
def hello2(event, context):
    r = requests.get("https://elastic.co")
    return {"statusCode": r.status_code, "body": "Success!"}


@capture_serverless()
def hello(event, context):
    metrics = get_client().metrics.register(MetricSet)
    time.sleep(0.15)

    metrics.gauge("TheAnswer").val = 42

    _do_work()

    body = {
        "message": "Hello world!",
        "event": event,
        "context": str(vars(context)),
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    print(response)

    print(json.dumps(event))

    return response


@capture_span()
def _do_work():
    time.sleep(0.35)
