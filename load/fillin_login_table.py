import boto3
from botocore.exceptions import ClientError

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("login")


def fillin_login_table():
    try:
        # Create 10 users
        items = []

        for i in range(10):
            item = {
                "email": f"s4066477{i}@student.rmit.edu.au",
                "user_name": f"ZhiHuiLu{i}",
                "password": f"{i}{(i+1)%10}{(i+2)%10}{(i+3)%10}{(i+4)%10}{(i+5)%10}"
            }
            items.append(item)

        # Insert into DynamoDB
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

        print("10 login records inserted successfully.")

    except ClientError as e:
        print("Error inserting data:")
        print(e)


if __name__ == "__main__":
    fillin_login_table()
