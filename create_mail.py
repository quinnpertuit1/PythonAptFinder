import json
import os
from datetime import datetime


class CreateMail:
    def __init__(self):
        # Intialize instance variables
        self.apt_folder = []
        self.html = ''
        self.unmatched_apts = []
        self.file_loc = os.path.dirname(os.path.abspath(__file__))

    # compare data and act on new data
    def compare_json(self):
        # open json files
        with open(self.file_loc + '/apt_original.json') as org_file:
            org_data = json.load(org_file)
        with open(self.file_loc + '/apt_latest.json') as latest_file:
            latest_data = json.load(latest_file)

        # Compare latest data to original
        temp_lat = latest_data['summary'][:]  # place list indices in array to remove in future iteration
        temp_org = org_data['summary'][:]
        for counter in range(len(latest_data['summary'])):
            shorten_latest = latest_data['summary'][counter]
            for counter2 in range(len(org_data['summary'])):
                shorten_org = org_data['summary'][counter2]
                if shorten_latest['name'] == shorten_org['name']:
                    apt_comparison = {'name': shorten_org['name'], 'update': int(shorten_latest['total']) - int(shorten_org['total'])}
                    self.apt_folder.append(apt_comparison)
                    temp_lat.remove(shorten_latest)
                    temp_org.remove(shorten_org)
        # change this
        self.unmatched_apts = temp_lat + temp_org
        print(self.unmatched_apts)

    # create html template for email
    def gen_html(self):
        # get today's date
        date = datetime.now().strftime('%A, %b %d')
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
            <h4>Here are your apartment updates for """+date+""":</h4>
           """
        # write html body
        for index in range(len(self.apt_folder)):
            # Check if updates are positive
            if self.apt_folder[index]['update'] > 0:
                update = '<span style="font-weight:bold; color: green;"> +' + str(self.apt_folder[index]['update']) + '</span>'
            elif self.apt_folder[index]['udpdate'] == 0:
                update = '<span style="font-weight:bold; color: black;"> +' + str(self.apt_folder[index]['update']) + '</span>'
            else:
                update = '<span style="font-weight:bold; color: red;">' + str(self.apt_folder[index]['update']) + '</span>'
            sub_body = "<p>"+self.apt_folder[index]['name'] + ":" + update + "</span></p>"
            html_body += sub_body
        for index in range(len(self.unmatched_apts)):
            update = '<span style="font-weight:bold;"> '+str(self.unmatched_apts[index]['total']) + '</span>'
            sub_body = "<p>"+self.unmatched_apts[index]['name'] + ":" + update + "</span></p>"
            html_body += sub_body
        html_foot = """
        </body>
        </html>
        """
        self.html = html_head + html_body + html_foot
        return self.html

if __name__ == '__main__':
    test = CreateMail()
    test.compare_json()
    test.gen_html()
