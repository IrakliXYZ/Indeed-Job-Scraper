from indeed import get_jobs as get_indeed_jobs
import csv

def main() -> None:
  jobs = get_indeed_jobs()

  with open('jobs.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Company", "Location", "Link"])

    for job in jobs:
      writer.writerow(job.values())

if __name__ == '__main__':
  main()

