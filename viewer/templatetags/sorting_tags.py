from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def sorted_url(context, sort_field):
    """
    Construiește URL-ul de sortare, păstrând parametrii de filtrare existenți.
    """
    request = context['request']
    current_sort = request.GET.get('sort', '-show_time') # Trebuie să se potrivească cu cel din view
    
    # Determină următoarea direcție de sortare
    new_sort_val = sort_field # Implicit, sortează ascendent
    if current_sort == sort_field:
        # Dacă deja sortăm ascendent, comutăm pe descendent
        new_sort_val = f"-{sort_field}"
    elif current_sort == f"-{sort_field}":
        # Dacă deja sortăm descendent, comutăm pe ascendent
        new_sort_val = sort_field
        
    # Copiază toți parametrii GET existenți (filtrele!)
    query_params = request.GET.copy()
    
    # Setează noul parametru de sortare
    query_params['sort'] = new_sort_val
    
    # Returnează string-ul de interogare (query string)
    return query_params.urlencode()

@register.simple_tag(takes_context=True)
def pagination_url(context, page_number):
    """
    Construiește URL-ul pentru paginare, păstrând TOȚI parametrii GET
    existenți (filtre, sortare) și doar suprascriind 'page'.
    """
    request = context['request']
    query_params = request.GET.copy()  # Copiază toți parametrii (sort, filter, etc.)
    query_params['page'] = page_number  # Setează sau suprascrie 'page'
    
    return query_params.urlencode()