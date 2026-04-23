import boto3
from botocore.exceptions import ClientError

# Create a DynamoDB resource in the default configured AWS region
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

def create_login_table():
    """
    Create the login table with:
    - Partition Key: email (String)
    The table stores:
    - email
    - user_name
    - password
    """
    table_name = "login"

    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    "AttributeName": "email",
                    "KeyType": "HASH"   # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "email",
                    "AttributeType": "S"
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )

        print(f"Creating table '{table_name}'...")
        table.wait_until_exists()
        print(f"Table '{table_name}' created successfully.")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "ResourceInUseException":
            print(f"Table '{table_name}' already exists.")
        else:
            print("Unexpected error while creating the table:")
            print(e)


if __name__ == "__main__":
    create_login_table()