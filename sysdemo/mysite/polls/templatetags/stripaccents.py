from django import template
import unicodedata
import json

register = template.Library()

# Register DB UTF Filter
@register.filter
def to_utf8(databases, data):
	other_values =[val.encode('utf8') for val in eval(data)]
	datalist = []
	for database in ['database_1','database_2','database_3','database_4','database_5']:
		if(database in other_values ):
			datalist.append(database)
		else:
			datalist.append("no_access")
	# return filter response as list 
	return [val.encode('utf8') for val in datalist]

# Manage the template query
@register.assignment_tag
def query(qs, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    return qs.filter(**kwargs)

# Convert the data to int
@register.filter()
def to_int(value):
    return int(value)


    # Register DB UTF Filter
@register.simple_tag
def template_error(data):
	data = [x.encode('utf8') for x in data]
	if "This field is required." in data:
		data.remove("This field is required.")
	if(len(data) > 0):
		return data
	else:
		return []

