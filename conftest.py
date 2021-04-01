import os
import boto3
import pytest
from moto import mock_sqs, mock_sns


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def sqs_client(aws_credentials):

    with mock_sqs():
        client = boto3.client("sqs", region_name='eu-north-1')
        yield client


@pytest.fixture
def sns_client(aws_credentials):

    with mock_sns():
        client = boto3.client("sns", region_name='eu-north-1')
        yield client


@pytest.fixture
def sqs_queue(sqs_client, aws_credentials):

    with mock_sqs():
        queue = sqs_client.create_queue(QueueName="test-queue")
        queue_url = queue['QueueUrl']
        queue_arn = sqs_client.get_queue_attributes(QueueUrl=queue_url)['Attributes']['QueueArn']

        yield {
            "QueueUrl": queue_url,
            "QueueArn": queue_arn
        }


@pytest.fixture
def sns_topic(sns_client, aws_credentials):
    with mock_sns():
        topic = sns_client.create_topic(Name="test-topic")
        topic_arn = topic['TopicArn']
        print(topic_arn)
        yield {
            "TopicArn": topic_arn
        }
