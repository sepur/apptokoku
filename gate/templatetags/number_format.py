from django import template
register = template.Library()
import re
from django.db.models import Q


#def get_query(query_string, search_fields):
#''' Returns a query, that is a combination of Q objects. That combination aims to search keywords within a model by 
#testing the given search fields.'''
#    query = None # Query to search for every search term
#    terms = normalize_query(query_string)
#    for term in terms:
#        or_query = None # Query to search for a given term in each field
#        for field_name in search_fields:
#            q = Q(**{"%s__icontains" % field_name: term})
#            if or_query is None:
#                or_query = q
#            else:
#                or_query = or_query | q
#        if query is None:
#            query = or_query
#        else:
#            query = query & or_query
#    return query

def get_query(query_string, search_fields):
    query = Q()
    terms = query_string.split()
    for term in terms:
        or_query = Q()
        for field_name in search_fields:
            or_query |= Q(**{f"{field_name}__icontains": term})
        query &= or_query
    return query

def normalize_query(query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def number_format(number, decimals=2, dec_point=',', thousands_sep='.'):
    try:
        number = round(float(number), decimals)
    except ValueError:
    	return number
    except TypeError:
        return number
    neg = number < 0
    integer, fractional = str(abs(number)).split('.')
    m = len(integer) % 3
    if m:
        parts = [integer[:m]]
    else:
        parts = []
    
    parts.extend([integer[m+t:m+t+3] for t in range(0, len(integer[m:]), 3)])
    
    if decimals:
        return '%s%s%s%s' % (
            neg and '-' or '', 
            thousands_sep.join(parts), 
            dec_point, 
            fractional.ljust(decimals, '0')[:decimals]
        )
    else:
        return '%s%s' % (neg and '-' or '', thousands_sep.join(parts))

register.filter(number_format)

def number_format_asura(number, decimals=2, dec_point=',', thousands_sep=','):
    try:
        number = round(float(number), decimals)
    except ValueError:
        return number
    except TypeError:
        return number
    neg = number < 0
    integer, fractional = str(abs(number)).split('.')
    m = len(integer) % 3
    if m:
        parts = [integer[:m]]
    else:
        parts = []

    parts.extend([integer[m+t:m+t+3] for t in xrange(0, len(integer[m:]), 3)])

    if decimals:
        return '%s%s%s%s' % (
            neg and '-' or '',
            thousands_sep.join(parts),
            dec_point,
            fractional.ljust(decimals, '0')[:decimals]
        )
    else:
        return '%s%s' % (neg and '-' or '', thousands_sep.join(parts))

register.filter(number_format_asura)
'''
def intWithCommas(x):
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)
register.filter(intWithCommas)
'''
