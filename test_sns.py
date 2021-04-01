import json
from moto import mock_sns, mock_sqs
from practice_sns import create_sns_topic, publish_to_sns_topic, subscribe_sns_to_sqs_topic, sns_with_sqs


@mock_sns
def test_sns_topic_creation(sns_client):

    topic_name = "Test-Topic"
    topic = create_sns_topic(sns_client, topic_name)
    assert topic["TopicArn"]
    assert topic["ResponseMetadata"]["HTTPStatusCode"] == 200
    assert topic_name in topic["TopicArn"]


@mock_sns
def test_publish_to_sns_topic(sns_client):

    topic = sns_client.create_topic(
        Name="Test-Topic-For-Sqs"
    )
    topic_arn = topic["TopicArn"]

    message = {"message": "Transaction is successful"}
    subject = "PURCHASE"
    publish = publish_to_sns_topic(sns_client, topic_arn, json.dumps(message), subject)

    assert publish['ResponseMetadata']['HTTPStatusCode'] == 200


@mock_sqs
@mock_sns
def test_sqs_subscription_to_sns(sns_client, sqs_client, sns_topic, sqs_queue):

    queue = sqs_client.create_queue(QueueName="test-queue")
    queue_url = queue['QueueUrl']
    queue_arn = sqs_client.get_queue_attributes(QueueUrl=queue_url)['Attributes']['QueueArn']

    topic = sns_client.create_topic(Name="test-topic")
    topic_arn = topic['TopicArn']

    response = subscribe_sns_to_sqs_topic(sns_client, queue_arn, topic_arn)
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200


@mock_sqs
@mock_sns
def test_sqs_with_sns(sns_client, sqs_client):
    queue = sqs_client.create_queue(QueueName="test-queue")
    queue_url = queue['QueueUrl']
    queue_arn = sqs_client.get_queue_attributes(QueueUrl=queue_url)['Attributes']['QueueArn']

    topic = sns_client.create_topic(Name="test-topic")
    topic_arn = topic['TopicArn']

    subscribe_sns_to_sqs_topic(sns_client, queue_arn, topic_arn)

    response = sns_with_sqs(sqs_client, sns_client, queue, topic, "Hello World!!")
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200
    assert response["Messages"][0]["Body"]["Message"] == "Hello World!!"

