import boto3
from botocore.exceptions import ClientError

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")


def delete_login_table():
    table_name = "login"

    try:
        table = dynamodb.Table(table_name)
        table.delete()

        print(f"Deleting table '{table_name}'...")
        table.wait_until_not_exists()
        print(f"Table '{table_name}' deleted successfully.")

    except ClientError as e:
        print("Error deleting table:")
        print(e)


if __name__ == "__main__":
    delete_login_table()
