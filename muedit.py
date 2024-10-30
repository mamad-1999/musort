import os
import subprocess
import sys
import argparse
from colorama import Fore, Style
from mutagen import File


def get_music_files(path):
    if os.path.isdir(path):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.mp3', '.wav', '.flac'))]
    elif os.path.isfile(path) and path.endswith(('.mp3', '.wav', '.flac')):
        return [path]
    else:
        print(f"{Fore.RED}Invalid path or unsupported file format.{Style.RESET_ALL}")
        sys.exit(1)


def display_metadata(filepath):
    music_file = File(filepath, easy=True)
    if not music_file:
        print(f"{Fore.RED}Unable to read metadata for: {filepath}{Style.RESET_ALL}")
        return {"title": "Unknown", "album": "Unknown", "artist": "Unknown"}

    title = music_file.get("title", ["Unknown"])[0]
    album = music_file.get("album", ["Unknown"])[0]
    artist = music_file.get("artist", ["Unknown"])[0]

    print(f"{Fore.CYAN}File: {os.path.basename(filepath)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'Title':<40}{'Album':<40}{'Artist':<40}{Style.RESET_ALL}")
    print(f"{title:<40}{album:<40}{artist:<40}")

    return {"title": title, "album": album, "artist": artist}


def update_metadata(filepath, title=None, album=None, artist=None):
    new_filename = filepath.rsplit(
        ".", 1)[0] + "_updated." + filepath.rsplit(".", 1)[1]
    cmd = ["ffmpeg", "-i", filepath, "-metadata", f"title={title or ''}",
           "-metadata", f"album={album or ''}", "-metadata", f"artist={artist or ''}",
           "-c", "copy", new_filename]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(filepath)
    print(f"{Fore.GREEN}Updated file created: {new_filename}{Style.RESET_ALL}")
    return new_filename


def main():
    parser = argparse.ArgumentParser(
        description="Edit metadata of music files interactively.")
    parser.add_argument(
        "path", help="Path to the music file or folder containing music files")
    parser.add_argument("--sort", action="store_true",
                        help="Sort files after editing by calling musort.py")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"{Fore.RED}The provided path does not exist.{Style.RESET_ALL}")
        sys.exit(1)

    music_files = get_music_files(args.path)
    for music_file in music_files:
        metadata = display_metadata(music_file)

        edit_choice = input(
            f"{Fore.MAGENTA}Edit metadata for {os.path.basename(music_file)}? (y/n): {Style.RESET_ALL}")
        if edit_choice.lower() != 'y':
            continue

        title = input(
            f"Enter Title [{metadata['title']}]: ").strip() or metadata['title']
        album = input(
            f"Enter Album [{metadata['album']}]: ").strip() or metadata['album']
        artist = input(
            f"Enter Artist [{metadata['artist']}]: ").strip() or metadata['artist']

        update_metadata(music_file, title, album, artist)

    # Call musort.py if --sort option is enabled
    if args.sort:
        sort_cmd = ["python", "musort.py", args.path,
                    "-f", "artist.title", "-s", "-"]
        subprocess.run(sort_cmd)
        print(f"{Fore.BLUE}Files sorted with musort.py{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
