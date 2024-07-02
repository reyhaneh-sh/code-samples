from typing import Dict, List, Any, TypeVar

T = TypeVar('T')


def decode_message(file_path: str) -> str:
    """
    Decodes a message file using a decoding map and pyramid indexing.
    :param file_path: Path to the message file containing key-value pairs
    :return: The decoded message as a string
    """
    decoding_map = get_message_map(file_path)
    pyramid_last_elements = get_pyramid_last_elements(len(decoding_map))
    message = get_decoded_message(pyramid_last_elements, decoding_map)
    return message


def get_message_map(file_path: str) -> Dict[int, str]:
    """
    Reads a message file and returns a decoding map as a dict.
    :param file_path: Path to the message file containing key-value pairs
    :return: A dictionary mapping integer keys to string values
    """
    decoding_map = {}
    with open(file_path, 'r') as file:
        lines = [line.rstrip() for line in file]
        for line in lines:
            key, value = line.split(' ')
            key = int(key)
            decoding_map[key] = value
    return decoding_map


def get_pyramid_last_elements(num_of_elements: int) -> List[int]:
    """
    Generates a list of last elements in each row of a numerical pyramid up to a given number of elements.
    :param num_of_elements: Total number of elements in the pyramid
    :return: A list containing the last element of each row in the pyramid
    """
    row_number = 1
    current_row_last_index = 1
    pyramid_last_elements = [current_row_last_index]
    while current_row_last_index < num_of_elements:
        row_number += 1
        current_row_last_index += row_number
        pyramid_last_elements.append(current_row_last_index)
    return pyramid_last_elements


def get_decoded_message(keys: List[T], decoding_map: Dict[T, Any]) -> str:
    """
    Decodes a message using a decoding map.
    :param keys: List of keys to decode
    :param decoding_map: A dictionary mapping keys to their respective values
    :return: The decoded message as a string
    """
    values = []
    for key in keys:
        values.append(decoding_map[key])
    message = ' '.join(values)
    return message


# Example usage:
if __name__ == '__main__':
    message_file_path = 'message_map.txt'
    decoded_message = decode_message(message_file_path)
    print(decoded_message)
