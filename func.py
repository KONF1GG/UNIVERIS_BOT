def string_is_digit(string):
    for letter in string:
        if letter.isdigit():
            return True
    else:
        return False
