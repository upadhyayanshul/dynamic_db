# import collectons

# DATA = { u'spam': u'eggs', u'foo': frozenset([u'Gah!']), u'bar': { u'baz': 97 },
#          u'list': [u'list', (True, u'Maybe'), set([u'and', u'a', u'set', 1])]}

# def convert(data):
#     if isinstance(data, basestring):
#         return str(data)
#     elif isinstance(data, collections.Mapping):
#         return dict(map(convert, data.iteritems()))
#     elif isinstance(data, collections.Iterable):
#         return type(data)(map(convert, data))
#     else:
#         return data

# print convert(DATA)


# DATA = { u'spam': u'eggs', u'foo': frozenset([u'Gah!']), u'bar': { u'baz': 97 },
#          u'list': [u'list', (True, u'Maybe'), set([u'and', u'a', u'set', 1])]}

# def to_utf8(d):

#     if type(d) is dict:
#         return { to_utf8(key):to_utf8(value) for key, value in d.items()}
#     elif type(d) is unicode:
#         return d.encode('utf8')
#     elif type(d) is list:
#        return [to_utf8(array) for array in d]
#     elif type(d) is tuple:
#         return tuple([to_utf8(tuple_data) for tuple_data in d])
#     elif type(d) is set:
#         return set([to_utf8(set_data) for set_data in tuple(d)])
#     elif type(d) is frozenset:
#         return frozenset([to_utf8(frozenset_data) for frozenset_data in tuple(d)])
#     else:
#         return d

# print to_utf8(DATA)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "demo",
    },
    'user': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': "USER",
    }
}
arr =["user","default"]
data = [ {db:DATABASES[db]['ENGINE'].split(".")[-1]} for db in DATABASES.keys() if db in arr ]
print("data,data",data,DATABASES.keys())