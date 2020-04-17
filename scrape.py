
try:
    import sys
    import os
    import datetime
    import requests
    from requests_html import HTML
    import pandas as pd

except Exception as e:
    print("Some modules are missing {}".format(e))


year = 2020
BASE_DIR = os.path.dirname(__file__)

# Saving Data into Html file
def url_to_text(url, filename="world.html", save=False):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        if save:
            html_text = r.text
            with open (f"world-{year}.html", 'w') as f:
                f.write(html_text)
        return html_text
    return ""


def parse_and_extract(url,name='2020'):

    html_text = url_to_text(url)
    # print(html_text)

    r_html = HTML(html=html_text)

    table_class = ".imdb-scroll-table"
    # table_class = "#table"
    r_table = r_html.find(table_class)

    # print(r_table)

    #Inspect Element >> ctrl+shift+p >> disable Javascript >> refresh


    table_data = []
    header_names = []
    if len(r_table) == 1:
        # print(r_table[0].text)
        parsed_table = r_table[0]
        rows = parsed_table.find("tr")
        header_row = rows[0]
        header_col = header_row.find('th')
        header_names = [x.text for x in header_col]
        
        for row in rows[1:]:
            #print(row.text)
            cols = row.find("td")
            row_data = []

            for i,col in enumerate(cols):
                #print(i,col.text,'\n\n')
                row_data.append(col.text)
            table_data.append(row_data)
        df = pd.DataFrame(table_data,columns=header_names)
        path = os.path.join(BASE_DIR,'data')
        os.makedirs(path,exist_ok=True)
        filepath = os.path.join('data',f'{name}.csv')
        df.to_csv(filepath,index=False)


# print(header_names)
# print(table_data)


def run(start_year=None,years_age=1):
    if start_year == None:
        now = datetime.datetime.now()
        start_year = now.year
    assert isinstance(start_year,int)
    assert isinstance(years_age,int)
    assert len(f"{start_year}") == 4
    for i in range(0,years_age+1):
        url = f'https://www.boxofficemojo.com/year/world/{start_year}'
        parse_and_extract(url=url,name=start_year)
        print(f"Finished {start_year}")
        start_year = start_year -1


if __name__ == "__main__": 
    try:
        start = int(sys.argv[1])
    except:
        start = None
    
    try:
        count = int(sys.argv[2])
    except:
        count = 1
    run(start_year=start,years_age=count)