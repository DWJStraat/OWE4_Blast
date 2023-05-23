from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_uniprot_id_from_html(html):
    """
    This function gets the UniProt ID from the HTML of the UniProt website
    :param html: the HTML of the UniProt website
    :return: the UniProt ID
    """
    site = urlopen(html)
    soup = BeautifulSoup(site, 'html.parser')
    elements = soup.find_all("div")
    return elements

a = get_uniprot_id_from_html(r"https://www.uniprot.org/uniprotkb/P04578/entry")