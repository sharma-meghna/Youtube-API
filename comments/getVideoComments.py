#!/usr/bin/python
# -*- coding: utf-8 -*-

# Sample Python code for youtube.comments.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python
import argparse
import re
from urllib.parse import urlparse
import os
import sys
import googleapiclient.discovery

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    parser = argparse.ArgumentParser(
        description='Get comments from videoId',
    )
    parser.add_argument("-v", "--videoid", type=str, help="your videoid or video link", required=True)
    parser.add_argument("-n", "--maxResults", default=20, type=int, help="max number of comments to fetch")
    parser.add_argument("-r", "--replies", action="store_true", help="get replies to comments")
    opts = parser.parse_args()
    url_data = urlparse(opts.videoid)

    VIDEO_ID = ""
    if url_data.query:
        result = re.search(r".*v=(.*?)(&|$)", url_data.query)    
        VIDEO_ID = result.group(1)
    else :
        VIDEO_ID = url_data.path.split("/")[-1]

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    DEVELOPER_KEY = os.getenv("GOOGLE_DEVELOPER_API_KEY", default=None)
    if DEVELOPER_KEY == None:
        print ("Error: Developer key not found")
        sys.exit(1)

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
            count += 1
            if (i["snippet"]["totalReplyCount"] and opts.replies):
                for j in i["replies"]["comments"]:
                    print (f'{j["snippet"]["authorDisplayName"]} replied - {j["snippet"]["textOriginal"]}')
                totalReplyCount = totalReplyCount + i["snippet"]["totalReplyCount"]
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
    print (f'Total Replies - ', (totalReplyCount))

if __name__ == "__main__":
    main()
