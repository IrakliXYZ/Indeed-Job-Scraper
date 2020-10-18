import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?as_and=Python+Developer+Intern&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=&fromage=any&limit={LIMIT}&sort=date&psf=advsrch&from=advancedsearch"


def get_last_page():
    results = requests.get(URL)
    soup = BeautifulSoup(results.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    return int(links[-2].string)


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


def extract_jobs(last_page):
    jobs = []
    
    for page in range(last_page):
        print(f"Scraping page #{page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

        for result in results:
            extraction_results = extraction(result)
            jobs.append(extraction_results)

    return jobs


def get_jobs():
    return extract_jobs(get_last_page())
