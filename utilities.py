from constants import (
    WEDNESDAY,
    IMAGES,
    IMAGE_FILE,
    VIDEO_FILE,
    USED_VIDEO_AND_IMAGES,
    VIDEO_INDEX,
    IMAGE_INDEX
)


def build_list(list_type: str):
    match list_type:
        case "images":
            list_to_use = IMAGES
            index = IMAGE_INDEX
            additional_file = IMAGE_FILE
        case "videos":
            list_to_use = WEDNESDAY
            index = VIDEO_INDEX
            additional_file = VIDEO_FILE
        case _:
            return []

    used_value = build_used_list(index)
    additional_values = None
    try:
        with open(additional_file, 'r') as file_handle:
            additional_values = file_handle.read()
    except FileNotFoundError:
        pass
    if additional_values:
        list_to_use.extend([x for x in additional_values.split(',') if x])

    trimmed_list = [x for x in list_to_use if x not in used_value]
    if not trimmed_list:
        clear_used_list(index)
        return build_list(list_type)
    return trimmed_list


def build_used_list(index=None):
    try:
        with open(USED_VIDEO_AND_IMAGES, 'r') as file_handle:
            used_dictionary = json.load(file_handle)
    except Exception as error:
        used_dictionary = {}
        print(f"No used file {error}")

    if not index:
        return used_dictionary
    return used_dictionary.get(index, [])


def mark_as_used(index, value):
    used_dictionary = build_used_list()
    used_list = used_dictionary.get(index)
    if not used_list:
        used_dictionary[index] = []
        used_list = used_dictionary[index]
    used_list.append(value)
    try:
        with open(USED_VIDEO_AND_IMAGES, 'w') as file_handle:
            json.dump(used_dictionary, file_handle)
    except Exception as error:
        print(f"Error writing used file: {error}")


def clear_used_list(index):
    used_dictionary = build_used_list()
    used_dictionary[index] = []
    try:
        with open(USED_VIDEO_AND_IMAGES, 'w') as file_handle:
            json.dump(used_dictionary, file_handle)
    except Exception as error:
        print(f"Error writing used file: {error}")
