from django import template

register = template.Library()


@register.filter(name="get_book_url")
def get_book_url(get_data, page=None):
    """
    Converts get parameter to url query
    :param get_data:
    :return:
    """
    string = "?"
    couter = 0
    for key, value in get_data.dict().items():
        if couter != 0:
            string += "&"
        if key == "page" and page is not None:
            string += f"page={str(page)}"
        else:
            string += f"{str(key)}={str(value)}"
        couter += 1
    return string
