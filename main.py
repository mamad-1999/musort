import os
import re
import argparse
import mutagen

# Define filter array for custom words/characters to remove from metadata fields
# Update this with actual terms
FILTER_TERMS = ["~", "UpMusic"]


def error_handler(message):
    print(f"Error: {message}")
    exit(1)


def clean_metadata_field(field):
    # Remove URLs or domain names
    field = re.sub(r'https?://\S+|www\.\S+|[\w\.-]+\.\w+', '', field)

    # Remove any term from the FILTER_TERMS array
    for term in FILTER_TERMS:
        field = field.replace(term, '')

    # Strip excess whitespace
    return field.strip()


def get_metadata_with_defaults(audio):
    # Extract metadata with default values if missing
    title = clean_metadata_field(audio.get('title', ["Music"])[0])
    artist = clean_metadata_field(audio.get('artist', ["Artist"])[0])
    album = clean_metadata_field(audio.get('album', ["Album"])[0])
    return title, artist, album


def construct_filename(format, title, artist, album, separator, count=None):
    # Construct the filename based on format and separator
    if format == "title.artist":
        name = f"{title}{separator}{artist}"
    elif format == "artist.title":
        name = f"{artist}{separator}{title}"
    elif format == "album.artist":
        name = f"{album}{separator}{artist}"
    elif format == "artist.album":
        name = f"{artist}{separator}{album}"
    elif format == "title.album":
        name = f"{title}{separator}{album}"
    elif format == "album.title":
        name = f"{album}{separator}{title}"
    else:
        name = title  # Default is just the title

    if count is not None:
        name = f"{count}{separator}{name}"

    return name


def process_file(file_path, format, separator):
    try:
        audio = mutagen.File(file_path, easy=True)
        if audio is None:
            error_handler(f"Could not read metadata from file: {file_path}")

        title, artist, album = get_metadata_with_defaults(audio)
        new_name = construct_filename(format, title, artist, album, separator)
        new_name = f"{new_name}{os.path.splitext(file_path)[1]}"

        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        print(f"Renamed file to: {new_name}")

    except Exception as e:
        error_handler(f"An error occurred while processing the file: {e}")


def process_folder(folder_path, format, separator):
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(
            os.path.join(folder_path, f))]
        count = 1

        for file_name in files:
            file_path = os.path.join(folder_path, file_name)

            audio = mutagen.File(file_path, easy=True)
            if audio is None:
                print(f"Skipping {file_name} (no metadata found)")
                continue

            title, artist, album = get_metadata_with_defaults(audio)
            new_name = construct_filename(
                format, title, artist, album, separator, count)
            new_name = f"{new_name}{os.path.splitext(file_name)[1]}"

            new_path = os.path.join(folder_path, new_name)
            os.rename(file_path, new_path)
            print(f"Renamed '{file_name}' to '{new_name}'")

            count += 1

    except Exception as e:
        error_handler(f"An error occurred while processing the folder: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Rename music files based on metadata")
    parser.add_argument("input", help="Path to the music file or folder")
    parser.add_argument("-f", "--format", choices=["title", "artist", "title.artist", "artist.title", "album.artist", "artist.album", "title.album", "album.title"],
                        default="title", help="Metadata field to use for renaming (default: Title)")
    parser.add_argument("-s", "--separator", default="-",
                        help="Separator between number and name (default: '-')")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        error_handler("The provided path does not exist.")

    if os.path.isfile(args.input):
        process_file(args.input, args.format, args.separator)
    elif os.path.isdir(args.input):
        process_folder(args.input, args.format, args.separator)
    else:
        error_handler(
            "Invalid input. Please provide a valid file or folder path.")


if __name__ == "__main__":
    main()
