def hash_to_byte(string):
    """
    Invert each hex group of a string to make it compatible with bytes
    :param string: hex string, no spaces
    :return: returns the inverted string
    """
    a = [string[i:i + 2] for i in range(0, len(string), 2)]
    reverse_a = a[::-1]
    return "".join(reverse_a)


if __name__ == "__main__":
    string = "0BE205E8"
    result = hash_to_byte(string)
