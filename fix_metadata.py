import os
import sys
import json

# Python script for fixing the metadata of images obtained from a Google Takeout archive.

def longest_common_prefix(string1, string2):
    """Return the longest common prefix of two strings."""
    common_prefix = ""
    for x, y in zip(string1, string2):
        if x == y:
            common_prefix += x
        else:
            break
    return common_prefix


def best_match(target, candidates):
    """Return the best match for a target string in a list of candidates.

    The best match is the candidate with the longest common prefix with the target."""
    best_match_length = 0
    best_match = None

    for candidate in candidates:
        common_prefix = longest_common_prefix(target, candidate)
        if len(common_prefix) > best_match_length:
            best_match_length = len(common_prefix)
            best_match = candidate

    return best_match

def find_corresponding_image(metadata_file, candidates):
    """Return the path of the image file corresponding to the given metadata file."""
    corresponding_image = os.path.splitext(metadata_file)[0]
    
    if corresponding_image not in filenames:
        corresponding_image = best_match(
            filename, [f for f in filenames if f != filename]
        )
        
    return os.path.join(dirpath, corresponding_image)


"""Iterate over all files in the given directory and set the modification time of the corresponding image file to the timestamp of the metadata file."""
root_path = sys.argv[1]

for dirpath, dirnames, filenames in os.walk(root_path):
    for filename in filenames:
        try:
            if not filename.endswith(".json"):
                continue

            if filename in [
                "Metadaten.json",
                "print-subscriptions.json",
                "shared_album_comments.json",
                "user-generated-memory-titles.json",
            ]:
                continue

            file_path = os.path.join(dirpath, filename)
            image_path = find_corresponding_image(filename, filenames)

            with open(file_path, "r") as json_file:
                metadata = json.load(json_file)
            timestamp = int(metadata["photoTakenTime"]["timestamp"])
            os.utime(image_path, (timestamp, timestamp))

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
