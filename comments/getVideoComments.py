# -*- coding: utf-8 -*-

# Sample Python code for youtube.comments.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python
import os
import googleapiclient.discovery

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAW6KLj4LiBLn-FucxwlNzZY2K_RSeiOdk"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=input("Please enter your video id")
    )
    response = request.execute()
    for i in response["items"]:
       print (f'{i["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]} says - {i["snippet"]["topLevelComment"]["snippet"]["textOriginal"]}')


if __name__ == "__main__":
    main()
