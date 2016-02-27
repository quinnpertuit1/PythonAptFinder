import json


class CreateMail:

    def __init__(self):
        self.apt_folder = []
        self.html = ""


    def gen_html(self):

        # Initialize html_body to store string literal containing html
        html_body = ''
        # Create string literal containing html head element
        html_head = html = """\
                <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>My Apartments</title>
            </head>
            <body>
           """
        for index in range(len(self.apt_folder)):
            sub_body = """
            <p>"""+self.apt_folder[index]['name']+"""</p>"""
            html_body += sub_body
        html_foot = """
        </body>
        </html>
        """
        self.html = html_head + html_body + html_foot
        print(self.html)
        return self.html


    # compare data and act on new data
    def compare_json(self):
        with open('apt_original.json') as org_file:
            org_data = json.load(org_file)
        with open('apt_latest.json') as latest_file:
            latest_data = json.load(latest_file)

        for counter in range(len(latest_data['summary'])):
            shorten_latest = latest_data['summary'][counter]
            for counter2 in range(len(org_data['summary'])):
                shorten_org = org_data['summary'][counter2]
                if shorten_latest['name'] == shorten_org['name']:
                    apt_comparison = {}
                    apt_comparison['name'] = shorten_org['name']
                    apt_comparison['update'] = int(shorten_latest['total']) - int(shorten_org['total'])
                    self.apt_folder.append(apt_comparison)
                    print(apt_comparison)


if __name__ == "__main__":
    test = CreateMail()
    test.compare_json()
