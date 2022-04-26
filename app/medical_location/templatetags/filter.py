from django import template
from bs4 import BeautifulSoup


register = template.Library()


@register.filter(name='split')
def split(value, key):
    """ Returns the value turned into a list. """
    link = value
    links = link.split(key)[8:]
    link_st = ""
    for link in links:
        if link == links[-1]:
            link_st = link_st + str(link)
        else:
            link_st = link_st + str(link) + "/"
    return link_st




@register.filter
def srt_to_list(value):
    soup = BeautifulSoup(value)
    get_text = soup.get_text()

    return

