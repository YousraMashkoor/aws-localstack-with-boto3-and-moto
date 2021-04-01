import boto3


def create_boto3_client(service_name):

    session = boto3.session.Session()
    client = session.client(
        service_name=service_name,
        endpoint_url='http://localhost:4566'
    )

    return client


def create_sqs_queue(sqs_client, queue_name):

    queue = sqs_client.create_queue(
        QueueName=queue_name,
        Attributes={'DelaySeconds': '5'}
    )
    # print(queue["attributes"]["QueueArn"])
    print(queue)

    return queue['QueueUrl']


def list_all_queue_urls(sqs_client):

    sqs_queues = sqs_client.list_queues()
    return sqs_queues["QueueUrls"]


if __name__ == "__main__":

    sqs = create_boto3_client('sqs')
    create_sqs_queue(sqs, 'my-queue')
