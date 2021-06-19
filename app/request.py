import urllib.request, json
from .models import Quote

def get_quotes():
   with urllib.request.urlopen('http://quotes.stormconsultancy.co.uk/random.json') as url:
    web_data = url.read()
    json_data = json.loads(web_data)

    if json_data.get('id'):
      author = json_data.get('author')
      quote = json_data.get('quote')

      new_quote = Quote(author, quote)
      return new_quote
    else:
      return 'No quote At the Moment'