import os
from google import genai
import webbrowser
from googleapiclient.discovery import build
from time import sleep
from colorama import Fore, Style, init
import sys
init()
with open("opened.txt", "w") as file:
    file.write("")
def display_welcome_message():
    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + "Welcome to MoodsMusic!".center(50))
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

def get_user_preferences():
    genre = input(Fore.YELLOW + "What genre of music do you prefer? " + Style.RESET_ALL)
    composer = input(Fore.YELLOW + "What composer do you prefer? " + Style.RESET_ALL)
    return genre, composer

def load_preferences():
    with open("opened.txt", "r+") as f:
        if f.read().strip() == "":
            display_welcome_message()
            input(Fore.YELLOW + "To start the setup process, press Enter" + Style.RESET_ALL)
            genre, composer = get_user_preferences()
            print(Fore.GREEN + "Thank you! MoodsMusic will shortly initiate!" + Style.RESET_ALL)
            print(Fore.CYAN + "Loading..." + Style.RESET_ALL)
            sleep(2)
            f.write(f"{genre},{composer}")
        else:
            f.seek(0)
            data = f.read().strip().split(",")
            genre, composer = data[0], data[1]
    return genre, composer

def youtube_search(song):
    try:
        youtube = build("youtube", "v3", developerKey="YOUR_API_KEY")
        request = youtube.search().list(q=song, part="snippet", maxResults=1, type="video")
        response = request.execute()
        for item in response["items"]:
            video_id = item["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            print(Fore.BLUE + f"Opening YouTube for the song: {song}" + Style.RESET_ALL)
            webbrowser.open(video_url)
    except Exception as e:
        print(Fore.RED + f"Error during YouTube search: {e}" + Style.RESET_ALL)

def music_generator(mood, genre, composer):
    try:
        client = genai.Client(api_key="YOUR_API_KEY")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                f"Gemini, your user is feeling this {mood} today.. He/She prefers {genre} music and {composer} as a composer. Just output a song that best fits this mood. Just give the name of the song, no other text, just the name of the song."
            ),
        )
        return response.text.strip()
    except Exception as e:
        print(Fore.RED + f"Error during music generation: {e}" + Style.RESET_ALL)
        sys.exit(1)

def main():
    genre, composer = load_preferences()
    mood = input(Fore.YELLOW + "Mood: " + Style.RESET_ALL)
    print(Fore.CYAN + "Generating song recommendation..." + Style.RESET_ALL)
    song = music_generator(mood, genre, composer)
    print(Fore.GREEN + f"Recommended Song: {song}" + Style.RESET_ALL)
    youtube_search(song)

if __name__ == "__main__":
    main()
