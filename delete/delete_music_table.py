# delete_music_table.py
import boto3
from botocore.exceptions import ClientError

def delete_music_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('music')
    
    try:
        print("Deleting table 'music'...")
        table.delete()
        
        # Wait for table to be completely deleted
        print("Waiting for table to be deleted...")
        table.wait_until_not_exists()
        print("Table 'music' has been successfully deleted.")
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("Table 'music' does not exist.")
        else:
            print(f"Error deleting table: {e}")

if __name__ == "__main__":
    delete_music_table()
