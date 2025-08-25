from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import pickle

# YouTube API scope (needed for managing playlists & likes)
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_authenticated_service():
    creds = None
    
    # Load saved login token if it exists
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no valid token, do the browser login flow
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the login token for reuse
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def get_liked_playlist_id(youtube):
    response = youtube.channels().list(
        part="contentDetails",
        mine=True
    ).execute()

    return response["items"][0]["contentDetails"]["relatedPlaylists"]["likes"]

def get_all_liked_videos(youtube, playlist_id):
    videos = []
    request = youtube.playlistItems().list(
        part="id,snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    while request:
        response = request.execute()
        for item in response["items"]:
            videos.append({
                "playlistItemId": item["id"],
                "title": item["snippet"]["title"]
            })
        request = youtube.playlistItems().list_next(request, response)

    return videos

def remove_liked_videos(youtube, videos, limit=100):
    count = 0
    for vid in videos:
        if count >= limit:   # Stop after 'limit' videos
            print(f"⏸️ Stopped after {limit} deletions (to avoid quota issues).")
            break
        try:
            youtube.playlistItems().delete(id=vid["playlistItemId"]).execute()
            print(f"Removed: {vid['title']}")
            count += 1
        except Exception as e:
            print(f"Error removing {vid['title']}: {e}")


if __name__ == "__main__":
    youtube = get_authenticated_service()
    liked_playlist_id = get_liked_playlist_id(youtube)
    print("Liked Playlist ID:", liked_playlist_id)

    videos = get_all_liked_videos(youtube, liked_playlist_id)
    print(f"Found {len(videos)} liked videos.")

    if videos:
        confirm = input("Do you really want to remove ALL liked videos? (y/n): ")
        if confirm.lower() == "y":
            remove_liked_videos(youtube, videos, limit=100)
            print("✅ All liked videos removed!")
        else:
            print("❌ Operation cancelled.")
    else:
        print("No liked videos found.")
