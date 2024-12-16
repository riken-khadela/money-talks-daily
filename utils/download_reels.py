from instagrapi.exceptions import UserNotFound

def download_popular_reel(cl, username):
    try:
        # Get the user ID by username
        user_id = cl.user_id_from_username(username)

        # Fetch user's media (including reels)
        user_medias = cl.user_medias(user_id, 20)  # Fetch the last 20 media items

        # Filter out only reels (IGTVs or videos)
        reels = [media for media in user_medias if media.media_type == 2]  # media_type 2 is video

        # Find the most popular reel based on likes or views
        if reels:
            popular_reel = max(reels, key=lambda r: r.like_count)  # Change to r.view_count for views
            
            # Download the reel
            reel_path = cl.video_download(popular_reel.pk)
            print(f"Reel downloaded to {reel_path}")
            return reel_path
        else:
            print(f"No reels found for {username}")
    except UserNotFound:
        print(f"User {username} not found.")
    return None

# Example usage
download_popular_reel('public_account_username')
