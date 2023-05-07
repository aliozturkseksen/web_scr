import requests
from bs4 import BeautifulSoup
import smtplib
import time


kariyer_url = 'https://www.kariyer.net/is-ilanlari/adana-ingilizce+ogretmeni'
yenibiris_url = 'https://www.yenibiris.com/is-ilanlari/adana+ingilizce-ogretmeni?siralama=uygunluk&sayfa-boyutu=100'
indeed_url = 'https://tr.indeed.com/jobs?q=ingilizce&l=Adana&sort=date&vjk=2877a17ee7e0113a'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def check_jobs():
    for url in [kariyer_url, yenibiris_url, indeed_url]:
        page = requests.get(url, headers=headers)
        soup1 = BeautifulSoup(page.content, 'html.parser')
        soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')
        results = soup2.find(id='resultsCol')
        if results is not None:
            job_elements = results.find_all('div', class_='jobsearch-SerpJobCard')
            for job_element in job_elements:
                title_element = job_element.find('a', class_='jobtitle')
                company_element = job_element.find('span', class_='company')
                location_element = job_element.find('span', class_='location')
                if 'adana' in location_element.get_text().lower() and 'ingilizce' in title_element.get_text().lower():
                    title = title_element.get_text().strip()
                    company = company_element.get_text().strip()
                    location = location_element.get_text().strip()
                    send_mail(f'{title} at {company}, located in {location}', url)
        else:
            print(f"Could not find job listings for {url}.")


def send_mail(title, url):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('ozguryilmazmaili@gmail.com', '159357Avax.')

    subject = f"{title} is now available at {url}"
    body = f"Check {url}"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'ozguryilmazmaili@gmail.com',
        'ingilizceogretmeni.ali@gmail.com',
        msg
    )
    print("HEY EMAIL HAS BEEN SENT!")
    server.quit()

while True:
    check_jobs()
    time.sleep(60*60*2) # scrape once every 2 hour
