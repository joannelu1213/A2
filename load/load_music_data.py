import json
import boto3
from botocore.exceptions import ClientError


# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("music")

def load_music_data(json_file_path):
    """Load songs from JSON file into DynamoDB"""
    import json
    
    table = dynamodb.Table("music")
    
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    loaded = 0
    errors = 0
    
    for song in data['songs']:
        item = {
            'artist': song['artist'],
            'title': song['title'],
            'title_album': f"{song['title']}#{song['album']}",
            'album': song['album'],
            'year': int(song['year']), 
            'image_url': song['img_url']
        }
        
        try:
            table.put_item(Item=item)
            loaded += 1
            print(f"Loaded: {song['artist']} - {song['title']} ({song['year']})")
        except ClientError as e:
            errors += 1
            print(f"Error loading {song['title']}: {e}")
    
    print(f"{loaded} loaded successfully, {errors} errors")


if __name__ == "__main__":
    load_music_data("data/2026a2_songs.json")  
