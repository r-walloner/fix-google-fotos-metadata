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


def select_meta_file(image_filename, candidate_filenames):
    """Return the path of the metadata file corresponding to the given image file."""
    meta_filename = os.path.splitext(image_filename)[0]

    if meta_filename not in candidate_filenames:
        meta_filename = best_match(image_filename, candidate_filenames)

    return meta_filename


"""Iterate over all files in the given directory and set the modification time of the corresponding image file to the timestamp of the metadata file."""
root_path = sys.argv[1]

for dirpath, dirnames, filenames in os.walk(root_path):
    meta_filenames = []
    image_filenames = []

    for file in filenames:
        if os.path.splitext(file)[1] == ".json":
            meta_filenames.append(file)
        else:
            image_filenames.append(file)

    for image in image_filenames:
        try:
            image_path = os.path.join(dirpath, image)
            meta_path = os.path.join(dirpath, select_meta_file(image, meta_filenames))

            with open(meta_path, "r") as meta_file:
                metadata = json.load(meta_file)
                timestamp = int(metadata["photoTakenTime"]["timestamp"])
                os.utime(image_path, (timestamp, timestamp))

        except Exception as e:
            print(f"Error processing {image_path}: {type(e).__name__}: {e}")
