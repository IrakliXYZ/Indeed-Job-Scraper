import requests
from bs4 import BeautifulSoup

INDEED_URL = "https://www.indeed.com/jobs?as_and=Python+Developer+Intern&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=&fromage=any&limit=50&sort=date&psf=advsrch&from=advancedsearch"

def extract_indeed_pages():
  results = requests.get(INDEED_URL)

  soup = BeautifulSoup(results.text, "html.parser")

  pagination = soup.find("div", {"class": "pagination"})


  links = pagination.find_all('a')

  pages = []

  for link in links[0:-1]:
    pages.append(int(link.string))

  max_pages = pages[-1]
  return max_pages
