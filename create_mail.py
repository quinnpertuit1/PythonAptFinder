__author__ = 'William Johnson'
import json
from scrape import ScrapeAPI

def gen_html():

    # Initialize html_body to store string literal containing html
    html_body = ''

    # read saved data from json file containing API data
    with open('test.json') as file:
        apt_data = json.load(file)
    # read current data from API
    current_API = ScrapeAPI()
    current_apts = current_API.get_data()

    # Create string literal containing html head element
    html_head = html = """\
            <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>My Apartments</title>
        </head>
        <body>
        <table>
        <caption>Apartment Summary</caption>
        <thead>
        <tr>
            <th>
                Type
            </th>
            <th>
                Floor Plans Avail.
            </th>
        </tr>
        </thead>
        <tbody>
       """
    for index in range(len(apt_data['summary'])):
        sub_body = """
            <tr>
                <td>""" + apt_data['summary'][index]['name'] + """</td>
                <td>""" + apt_data['summary'][index]['total'] + """</td>
            </tr>"""
        html_body += sub_body
    html = html_head + html_body
    print(current_apts)
    return html
    # compare data and act on new data
gen_html()