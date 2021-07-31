from datetime import datetime

def convert_datetime_to_iso(datetime_obj):
    """
    convert a given datetime object to string iso format
    :param datetime_obj: datetime object to convert
    :return: iso format (string) of the given datetime
    """
    if datetime_obj is None:
        return None
    return datetime_obj.isoformat() + 'Z'

def convert_iso_format_to_datetime(iso_format_str):
    """
    convert a given iso format string to datetime object
    :param iso_format_str: iso format in string to convert
    :return: datetime object represent the given iso format
    """
    if iso_format_str is None:
        return None
    return datetime.fromisoformat(iso_format_str.split('.')[0])
