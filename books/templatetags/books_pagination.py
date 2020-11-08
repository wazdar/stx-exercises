from django import template

register = template.Library()


@register.filter(name="get_book_url")
def get_book_url(get_data, page=None):
    """
    Converts get parameter to url query
    :param page:
    :param get_data:
    :return string:
    """
    string = "?"
    counter = 0
    get_dict = get_data.dict()

    if get_dict == {} and page is None or page == 0:
        return None

    if get_dict == {} or "page" not in get_data.keys():
        string += f"page={str(page)}&"

    for key, value in get_data.dict().items():
        if counter != 0:
            string += "&"
        if key == "page" and page is not None:
            string += f"page={str(page)}"
        else:
            string += f"{str(key)}={str(value)}"
        counter += 1
    return string
