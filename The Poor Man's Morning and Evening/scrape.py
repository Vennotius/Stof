from bs4 import BeautifulSoup
from datetime import datetime

class Devotional:
    def __init__(self, date, time_of_day, scripture_reference, scripture_quote, content):
        self.date = date
        self.time_of_day = time_of_day
        self.scripture_reference = scripture_reference
        self.scripture_quote = scripture_quote
        self.content = content

    def __str__(self) -> str:
        return f"# {self.date} — {self.time_of_day}  \n## {self.scripture_reference}  \n### {self.scripture_quote}  \n{self.content}\n\n"


def scrape_devotional(html):
    soup = BeautifulSoup(html, 'html.parser')
    devotionals = []

    headers = soup.find_all('h3', class_='s7')
    for header in headers:
        date_text = header.text.strip().replace('\n', ' ')
        parts = date_text.split('—')
        if len(parts) == 3:
            date_str = parts[0].strip()
            time_of_day = parts[1].strip().lower()
            scripture_reference = parts[2].strip()

            # Parse the date (assuming the year is known, e.g., 2024)
            date = datetime.strptime(f'2024 {date_str}', '%Y %B %d').date()

            # Get the content associated with this header
            content = ''
            scripture_quote = None
            for sibling in header.find_next_siblings():
                if sibling.name == 'h3':
                    break
                if sibling.name == 'p':
                    if scripture_quote:
                        content += sibling.get_text().replace('\n', ' ') + '\n'
                    else:
                        scripture_quote = sibling.get_text().replace('\n', ' ')

            devotional = Devotional(
                date=date,
                time_of_day=time_of_day,
                scripture_reference=scripture_reference,
                scripture_quote=scripture_quote.replace('—', ' — '),
                content=content.replace('—', ' — ').strip()
            )
            devotionals.append(devotional)

    return devotionals


file_path = '000.html'  # Replace with the actual file path

with open(file_path, 'r', encoding='utf-8') as file:
    html = file.read()

devotionals = scrape_devotional(html)
for devotional in devotionals:
    #print(devotional.date)
    if devotional.date == datetime.today().date():
        print(devotional)

with open('poormans.md', 'w', encoding='utf-8') as file:
    # Write each line to the file
    for devotional in devotionals:
        file.write(str(devotional) + '\n') 


from datetime import date
def to_dict(devotional):
        return {
            'date': devotional.date.isoformat() if isinstance(devotional.date, date) else devotional.date,
            'time_of_day': devotional.time_of_day,
            'scripture_reference': devotional.scripture_reference,
            'scripture_quote': devotional.scripture_quote,
            'content': devotional.content
        }


import json
# Convert the list of objects to a list of dictionaries
devotionals_dict = [to_dict(devotional) for devotional in devotionals]

# Specify the output file name
filename = "The Poor Man's Morning and Evening Portion - Robert Hawker.json"

# Write the list of dictionaries to a JSON file with UTF-8 encoding
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(devotionals_dict, file, ensure_ascii=False, indent=4)