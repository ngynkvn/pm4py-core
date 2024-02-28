import sys


def indent_representation(model_string, max_indent=sys.maxsize):
    model_string = model_string.replace('\n', '').replace('\r', '').replace('\t', '').strip()

    indent_level = 0
    list_strs = []
    formatted_str = ""
    for char in model_string:
        if char in '({':
            formatted_str += char
            indent_level += 1
            if indent_level <= max_indent:
                list_strs.append(formatted_str)
                formatted_str = '\t' * indent_level
        elif char in ')}':
            indent_level -= 1
            if indent_level < max_indent:
                if formatted_str[-1] not in '({':
                    list_strs.append(formatted_str)
                    formatted_str = '\t' * indent_level
            formatted_str += char
        elif char == ',':
            formatted_str += char
            if indent_level <= max_indent:
                list_strs.append(formatted_str)
                formatted_str = '\t' * indent_level
        else:
            formatted_str += char
    list_strs.append(formatted_str)
    return list_strs
