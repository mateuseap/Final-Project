from fastbook import *
def my_search(term,max_images): # for some reason, it is not downloading the correct number of images, but it's enough
  
  "Search for `term` with DuckDuckGo and return a unique urls of about `max_images` images"
  assert max_images<1000
  url = 'https://duckduckgo.com/'
  res = urlread(url,data={'q':term})
  searchObj = re.search(r'vqd=([\d-]+)\&', res)
  assert searchObj
  requestUrl = url + 'i.js'
  params = dict(l='us-en', o='json', q=term, vqd=searchObj.group(1), f=',,,', p='1', v7exp='a')
  urls,data = set(),{'next':1}
  while len(urls)<max_images and 'next' in data:
      try:
          data = urljson(requestUrl,data=params)
          urls.update(L(data['results']).itemgot('image'))
          requestUrl = url + data['next']
      except (URLError,HTTPError): pass
      time.sleep(0.2)

  return L(urls) 

dog_types = 'Shihtzu','Pug'
path = Path('/content/gdrive/MyDrive/caes')
for o in dog_types:
    dest = (path/o)
    #dest.mkdir(exist_ok=True)
    urls = my_search(o ,150)
    download_images(dest, urls=urls)
