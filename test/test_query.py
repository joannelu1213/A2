
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("music")


def print_results(test_name, items):
    print(f"\n--- {test_name} ---")
    if not items:
        print("No results found.")
        return

    for item in items:
        title = item.get("title", "N/A")
        artist = item.get("artist", "N/A")
        album = item.get("album", "N/A")
        year = item.get("year", "N/A")
        print(f"{title} - {artist} - {album} - {year}")


def test_query_by_artist():
    """Base table query: get all songs by an artist"""
    response = table.query(
        KeyConditionExpression=Key("artist").eq("Taylor Swift")
    )
    print_results("Test 1: Songs by Taylor Swift", response["Items"])


def test_query_by_artist_year():
    """LSI query: get songs by artist in a specific year"""
    response = table.query(
        IndexName="artist-year-index",
        KeyConditionExpression=Key("artist").eq("Taylor Swift") & Key("year").eq(2017)
    )
    print_results("Test 2: Taylor Swift songs in 2017", response["Items"])


def test_query_by_artist_album():
    """LSI query: get songs by artist from a specific album"""
    response = table.query(
        IndexName="artist-album-index",
        KeyConditionExpression=Key("artist").eq("Taylor Swift") & Key("album").eq("Reputation")
    )
    print_results("Test 3: Taylor Swift songs from album 'Reputation'", response["Items"])


def test_query_by_album():
    """GSI query: get all songs from an album"""
    response = table.query(
        IndexName="album-title-index",
        KeyConditionExpression=Key("album").eq("Reputation")
    )
    print_results("Test 4: Songs from album 'Reputation'", response["Items"])


def test_query_by_year():
    """GSI query: get all songs released in a given year"""
    response = table.query(
        IndexName="year-index",
        KeyConditionExpression=Key("year").eq(2012)
    )
    print_results("Test 5: Songs released in 2012", response["Items"])


def test_query_by_title():
    """GSI query: get all songs with a given title"""
    response = table.query(
        IndexName="title-index",
        KeyConditionExpression=Key("title").eq("Delicate")
    )
    print_results("Test 6: Songs with title 'Delicate'", response["Items"])


def main():
    try:
        test_query_by_artist()
        test_query_by_artist_year()
        test_query_by_artist_album()
        test_query_by_album()
        test_query_by_year()
        test_query_by_title()

    except ClientError as e:
        print("DynamoDB query error:")
        print(e.response["Error"]["Message"])

    except Exception as e:
        print("Unexpected error:")
        print(str(e))


if __name__ == "__main__":
    main()
