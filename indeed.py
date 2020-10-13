import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?as_and=Python+Developer+Intern&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=&fromage=any&limit={LIMIT}&sort=date&psf=advsrch&from=advancedsearch"

def extract_indeed_pages():
  results = requests.get(URL)

  soup = BeautifulSoup(results.text, "html.parser")

  pagination = soup.find("div", {"class": "pagination"})


  links = pagination.find_all('a')

  pages = []

  for link in links[0:-1]:
    pages.append(int(link.string))

  max_pages = pages[-1]
  return max_pages


def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    result = requests.get(f"{URL}&start={page*LIMIT}")

    soup = BeautifulSoup(result.text, "html.parser")

    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

    for result in results:
      title = result.find("a", {"class": "jobtitle"})["title"]

      print(title)

  return jobs