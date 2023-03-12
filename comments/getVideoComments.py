#!/usr/bin/python
# -*- coding: utf-8 -*-

# Sample Python code for youtube.comments.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python
import argparse
import os
import sys
import googleapiclient.discovery

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    parser = argparse.ArgumentParser(
        description='Get comments from videoId',
    )
    parser.add_argument("-v", "--videoid", type=str, help="your videoid", required=True)
    parser.add_argument("-n", "--maxResults", default=20, type=int, help="max number of comments to fetch")
    opts = parser.parse_args()

    VIDEO_ID = opts.videoid

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAW6KLj4LiBLn-FucxwlNzZY2K_RSeiOdk"

    totalReplyCount = 0
    count = 0

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    request = youtube.commentThreads().list(
        part="snippet,replies",
        maxResults=opts.maxResults,
        videoId=VIDEO_ID
    )
    response = request.execute()
    
    while (True):        
        for i in response["items"]:
            print (f'{i["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]} says - {i["snippet"]["topLevelComment"]["snippet"]["textOriginal"]}')
            totalReplyCount = totalReplyCount + i["snippet"]["totalReplyCount"]
            count += 1
        if ("nextPageToken" not in response) or count >= opts.maxResults:
            break
        remaining = opts.maxResults - count
        request = youtube.commentThreads().list(
            part="snippet,replies",
            maxResults=remaining,
            videoId=VIDEO_ID,
            pageToken=response["nextPageToken"]
        )

        response = request.execute()
   
    print (f'Total Comments - ', (count))

if __name__ == "__main__":
    main()
