from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
root=Path(__file__).resolve().parent/'dist'
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key not in ('href','src') or not value:continue
   parsed=urlsplit(value)
   if parsed.scheme or parsed.netloc or not parsed.path:continue
   path=root/unquote(parsed.path.lstrip('/')) if parsed.path.startswith('/') else self.page.parent/unquote(parsed.path)
   if parsed.path.endswith('/'):path=path/'index.html'
   assert path.is_file(),f'{self.page}: {value}'
for page in root.rglob('*.html'):
 parser=Links();parser.page=page;parser.feed(page.read_text())
print('Ověřeny odkazy a lokální soubory všech HTML stránek.')
