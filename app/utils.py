from django.db.models import Q

def search_in_model(model, search_string):
    """
    Search in all text-based fields of a model for a substring.
    
    :param model: The model class you want to search.
    :param search_string: The string you want to search for in all fields.
    :return: Queryset of model objects that match the search string in any field.
    """
    search_string = search_string.strip()
    query = Q()
    # Get all fields in the model
    for field in model._meta.get_fields():
        # Check if the field is a CharField or TextField (fields that can contain text)
        if field.get_internal_type() in ['CharField', 'TextField']:
            # Dynamically create a Q object for icontains lookup on each field
            for string in search_string.split(' '):
              query |= Q(**{f"{field.name}__icontains": string.strip()})
    
    # Return a queryset filtered by the combined query
    print(query)
    return model.objects.filter(query)