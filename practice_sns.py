import boto3


def create_sns_topic(sns, topic_name, attributes={}):
    topic = sns.create_topic(
        Name=topic_name,
        Attributes=attributes
    )
    return topic


def publish_to_sns_topic(sns_client, topic_arn, message, subject):

    publish = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject
    )
    return publish


def subscribe_sns_to_sqs_topic(sns_client, queue_arn, topic_arn):

    subscription = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='sqs',
        Endpoint=queue_arn
    )

    # print(subscription)
    return subscription


def sns_with_sqs(sqs_client, sns_client, queue, topic, message):

    queue_url = queue['QueueUrl']
    topic_arn = topic['TopicArn']

    publish = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject="PURCHASE STATUS"
    )

    res = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1
    )

    message = res['Messages'][0]['Body']
    print(message)
    return res


if __name__ == "__main__":
    # sns_with_sqs()
    sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')
    sns = boto3.client('sns', endpoint_url='http://localhost:4566')

    topic_arn = sns.create_topic(Name='Test-Topic')['TopicArn']
    queue_url = sqs.create_queue(QueueName='Test-Queue')['QueueUrl']
    queue_arn = sqs.get_queue_attributes(QueueUrl=queue_url)['Attributes']['QueueArn']

    subscribe_sns_to_sqs_topic(sns, queue_arn, topic_arn)
