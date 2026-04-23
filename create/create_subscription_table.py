import boto3
from botocore.exceptions import ClientError

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")


def create_subscription_table():
    table_name = "subscriptions"

    try:
        table = dynamodb.create_table(
            TableName=table_name,

            KeySchema=[
                {"AttributeName": "email", "KeyType": "HASH"},         # Partition key
                {"AttributeName": "title_album", "KeyType": "RANGE"}   # Sort key
            ],

            AttributeDefinitions=[
                {"AttributeName": "email", "AttributeType": "S"},
                {"AttributeName": "title_album", "AttributeType": "S"}
            ],

            BillingMode="PAY_PER_REQUEST"
        )

        print(f"Creating table '{table_name}'...")
        table.wait_until_exists()
        print(f"Table '{table_name}' created successfully.")
        print("Primary Key: email + title_album")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "ResourceInUseException":
            print(f"Table '{table_name}' already exists.")
        else:
            print("Unexpected error while creating the table:")
            print(e)


if __name__ == "__main__":
    create_subscription_table()
