from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def get_html_soup(url):
    raw_html = simple_get(url)
    return BeautifulSoup(raw_html, 'html.parser')


def get_ica_recipe(url):
    html_soup = get_html_soup(url)

    ingreds = []

    for tag in html_soup.find_all("span", "ingredient"):
        amount = tag.get('data-amount')
        unit = tag.get('data-type')
        item = tag.string

        item = item.replace(amount, '').replace(unit, '')

        amount = amount.replace(',', '.')

        ingreds.append((amount, unit, item))

    name = html_soup.title.string.replace("| Recept ICA.se", "").strip()
    return name, ingreds


def get_koket_recipe(url):
    html_soup = get_html_soup(url)

    ingreds = []

    for tag in html_soup.find_all("span", "ingredient"):
        amount_unit = tag.contents[0].string
        item = tag.contents[1].string

        if amount_unit is None:
            amount = None
            unit = ""

        else:
            amount_unit_list = amount_unit.split()

            if len(amount_unit_list) > 1:
                amount = amount_unit_list[0].replace(',', '.')
                unit = amount_unit_list[1]

            elif len(amount_unit_list) == 1:
                amount = amount_unit_list[0].replace(',', '.')
                unit = ""

            else:
                amount = None
                unit = ""

        ingreds.append((amount, unit, item))

    name = html_soup.title.string.replace("| Recept från Köket.se", "").strip()
    return name, ingreds


def get_coop_recipe(url):
    html_soup = get_html_soup(url)

    ingreds = []

    for tag in html_soup.find_all("li", "Recipe-ingredient"):
        item = tag.find("span", "Recipe-ingredientType").string
        amount_unit = tag.find("span", "Recipe-ingredientAmount").string

        if amount_unit is None:
            amount = None
            unit = ""

        else:
            amount_unit_list = amount_unit.split()

            if len(amount_unit_list) > 1:
                amount = amount_unit_list[0].replace(',', '.')
                unit = amount_unit_list[1]

            elif len(amount_unit_list) == 1:
                amount = amount_unit_list[0].replace(',', '.')
                unit = ""

            else:
                amount = None
                unit = ""

        ingreds.append((amount, unit, item))

    name = html_soup.title.string.strip()
    return name, ingreds


def parse_recipe_from_url(html_address):
    if "www.ica.se" in html_address:
        recipe_name, ingreds = get_ica_recipe(html_address)
    elif "www.coop.se" in html_address:
        recipe_name, ingreds = get_coop_recipe(html_address)
    elif "www.koket.se" in html_address:
        recipe_name, ingreds = get_koket_recipe(html_address)
    else:
        recipe_name = ""
        ingreds = ""

    if ingreds:
        parse_successful = True
    else:
        parse_successful = False

    return recipe_name, ingreds, parse_successful


if __name__ == "__main__":
    #from_url = 'https://www.ica.se/recept/fryst-cheesecake-med-saffran-722867/'
    #from_url = 'https://www.coop.se/Recept--mat/Recept/l/lax-med-chunky-pesto-och-tagliatelle/'
    from_url = 'https://www.koket.se/sara_begner/soppor_och_grytor/korv_och_chark/korv_stroganoff/'
    recipe_title, recipe_ingreds, success = parse_recipe_from_url(from_url)
    print("Success: ", success)
    print(recipe_title)
    print(recipe_ingreds)
