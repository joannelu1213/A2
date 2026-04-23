"""
Task 2: Create 'Music' Table in DynamoDB
"""
import boto3
from botocore.exceptions import ClientError

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

def create_music_table():
    table_name = "music"

    try:
        table = dynamodb.create_table(
            TableName=table_name,

            # Define key schema
            KeySchema=[
                {"AttributeName": "artist", "KeyType": "HASH"},    # Partition key
                {"AttributeName": "title_album", "KeyType": "RANGE"}     # Sort key 
            ],

            # Define all attributes used in the table keys and indexes
            AttributeDefinitions=[
                {"AttributeName": "artist", "AttributeType": "S"},
                {"AttributeName": "title", "AttributeType": "S"},    
                {"AttributeName": "year", "AttributeType": "N"},
                {"AttributeName": "album", "AttributeType": "S"},
                {"AttributeName": "title_album", "AttributeType": "S"}
            ],

            # Define Local Secondary Index (LSI)
            # Same partition key as the main table: artist
            # Different sort key: year
            LocalSecondaryIndexes=[
                {
                    "IndexName": "artist-year-index",
                    "KeySchema": [
                        {"AttributeName": "artist", "KeyType": "HASH"},
                        {"AttributeName": "year", "KeyType": "RANGE"}
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                },
                # LSI for artist-album queries (required for spec)
                {
                    "IndexName": "artist-album-index",
                    "KeySchema": [
                        {"AttributeName": "artist", "KeyType": "HASH"},
                        {"AttributeName": "album", "KeyType": "RANGE"}
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                }
            ],

            # Define Global Secondary Index (GSI)
            
            # GSI for album queries
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "album-title-index",
                    "KeySchema": [
                        {"AttributeName": "album", "KeyType": "HASH"},
                        {"AttributeName": "title", "KeyType": "RANGE"}
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                },
                # GSI for year queries
                {
                    "IndexName": "year-index",
                    "KeySchema": [
                        {"AttributeName": "year", "KeyType": "HASH"},
                        {"AttributeName": "artist", "KeyType": "RANGE"}
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                },
                #GSI for title queries
            
                {
                    "IndexName": "title-index",
                    "KeySchema": [
                        {"AttributeName": "title", "KeyType": "HASH"},
                        {"AttributeName": "artist", "KeyType": "RANGE"}
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    }
                }
            ],

            BillingMode="PAY_PER_REQUEST"
        )


        print(f"Creating table '{table_name}'...")
        table.wait_until_exists()
        print(f"Table '{table_name}' created successfully.")
        print("\nIndexes created:")
        print("- Primary Key: artist + title_album")
        print("- LSI: artist-year-index")
        print("- LSI: artist-album-index")
        print("- GSI: album-title-index")
        print("- GSI: year-index")
        print("- GSI: title-index")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "ResourceInUseException":
            print(f"Table '{table_name}' already exists.")
        else:
            print("Unexpected error while creating the table:")
            print(e)



if __name__ == "__main__":
    create_music_table()



