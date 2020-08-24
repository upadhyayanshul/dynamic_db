## HANDLE UNICODE DATA FROM THE QUERY IN DJANGO ##
def to_utf8(data_to_parse):

    if type(data_to_parse) is dict:
        return { to_utf8(key):to_utf8(value) for key, value in data_to_parse.items()}
    elif type(data_to_parse) is unicode:
        return data_to_parse.encode('utf8')
    elif type(data_to_parse) is list:
       return [to_utf8(array) for array in data_to_parse]
    elif type(data_to_parse) is tuple:
        return tuple([to_utf8(tuple_data) for tuple_data in data_to_parse])
    elif type(data_to_parse) is set:
        return set([to_utf8(set_data) for set_data in tuple(data_to_parse)])
    elif type(data_to_parse) is frozenset:
        return frozenset([to_utf8(frozenset_data) for frozenset_data in tuple(data_to_parse)])
    else:
        return data_to_parse