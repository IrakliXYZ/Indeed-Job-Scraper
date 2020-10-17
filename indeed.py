import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?as_and=Python+Developer+Intern&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=&fromage=any&limit={LIMIT}&sort=date&psf=advsrch&from=advancedsearch"

def get_last_page() -> int:
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')

    pages = [int(link.string) for link in links[0:-1]]
    return pages[-1]


def extraction(result: object) -> dict:
    title = result.find("a", {"class": "jobtitle"})["title"]

    company = result.find("span", {"class": "company"})
    company_anchor = company.find("a")

    if company_anchor:
        company = company_anchor.string.strip() 
    else: 
        company = company.string.strip()

    location = result.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    link_id = result["data-jk"]

    return {
        'title'     : title,
        'company'   : company,
        'location'  : location,
        'link'      : f'https://www.indeed.com/viewjob?jk={link_id}'
    }


def extract_jobs(last_page: int) -> list:
    jobs = []

    for page in range(last_page):
        print(f"Scraping page #{page}")

        result = requests.get(f"{URL}&start={page*LIMIT}")

        soup = BeautifulSoup(result.text, "html.parser")

        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        jobs += [extraction(result) for result in results]
        
    return jobs


def get_jobs() -> list:
    last_page = get_last_page()
    return extract_jobs(last_page)