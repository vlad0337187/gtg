import re


def extract_tags_from_text(text):
    """ Given a string, returns a list of the @tags contained in that """
    return re.findall(r'(?:^|[\s])(@[\w\/\.\-\:\&]*\w)', text)


def parse_tag_list(text):
    """ Parse a line of a list of tasks. User can specify if the tag is
    positive or not by prepending '!'.

    @param  text:  string entry from user
    @return: list of tupples (tag, is_positive)
    """
    result = []
    for tag in text.split():
        if tag.startswith('!'):
            tag = tag[1:]
            is_positive = False
        else:
            is_positive = True

        if not tag.startswith('@'):
            tag = "@" + tag

        result.append((tag, is_positive))
    return result
