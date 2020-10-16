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


def extraction(result):
    title = result.find("a", {"class": "jobtitle"})["title"]

    company = result.find("span", {"class": "company"})
    company_anchor = company.find("a")

    if company_anchor is not None:
        company = (company_anchor.string.strip())
    else:
        company = (company.string.strip())

    location = result.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    link_id = result["data-jk"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://www.indeed.com/viewjob?jk={link_id}"
    }


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&start={page*LIMIT}")

        soup = BeautifulSoup(result.text, "html.parser")

        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

        for result in results:
            extraction_results = extraction(result)
            jobs.append(extraction_results)

    return jobs
