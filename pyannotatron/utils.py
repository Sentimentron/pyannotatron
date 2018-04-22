import os
import datetime
import base64

def parse_json_date(input):
    if type(input) == datetime.datetime:
        return input
    else:
        return datetime.datetime.strptime(input, '%Y-%m-%dT%H:%M:%S.%fZ')


def date_to_json(input: datetime.datetime):
    # TODO: timezones
    return input.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def base64_to_bytes(input: str) -> bytes:
    return base64.b64decode(input)


def bytes_to_base64(input: bytes) -> str:
    return base64.b64encode(input).decode("utf8")


def generic_from_json(json_dict, mapping_dict):
    response_dict = {}
    for key in json_dict:
        old_value = json_dict[key]
        if key not in mapping_dict:
            response_dict[key] = json_dict[key]
            continue

        def conversion_func(x):
            return x

        try:
            new_key, conversion_func, _ = mapping_dict[key]
        except ValueError:
            new_key = mapping_dict[key]
            assert type(new_key) != type([])

        response_dict[new_key] = conversion_func(old_value)

    return response_dict


def generic_to_json(python_dict, mapping_dict):
    response_dict = {}
    converted_keys = set([])
    for key in mapping_dict:

        def conversion_func_raw(x):
            return x

        try:
            python_name, _, conversion_func = mapping_dict[key]
        except ValueError:
            conversion_func = conversion_func_raw
            python_name = mapping_dict[key]

        if python_name in python_dict:
            value = python_dict[python_name]
            response_dict[key] = conversion_func(value)
            converted_keys.add(python_name)

    for key in python_dict:
        if key in converted_keys:
            continue
        matched = False
        for potential_key in mapping_dict:
            try:
                python_name, _, _ = mapping_dict[potential_key]
            except ValueError:
                python_name = mapping_dict[potential_key]
            matched |= python_name == key
        if not matched:
            response_dict[key] = python_dict[key]

    return response_dict
