from bs4 import BeautifulSoup
import requests
import json
from utils import convert_hhmarkets_to_oneappmarkets,EXPERIENCE_DICTIONARY


API_ROOT_URL = 'https://api.hh.ru/'
SEARCH_PERIOD = 1
VACANCIES_URL = 'https://hh.ru/search/vacancy?enable_snippets=true&ored_clusters=true&order_by=publication_time'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
}


def get_vacancy_data(vacancy_id):
    url = API_ROOT_URL + 'vacancies/' + vacancy_id
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        return None
def get_vacancies():
    vacancies = []
    response = requests.get(VACANCIES_URL,params={'search_period':SEARCH_PERIOD},headers=HEADERS)
    if response.status_code == requests.codes.ok:
        html_document = BeautifulSoup(response.text,'html.parser')
        vacancy_items = html_document.find_all('div',class_='serp-item')
        for vacancy_item in vacancy_items:
            title_tag = vacancy_item.find('a',class_='serp-item__title')
            title_text = title_tag.text.strip()
            title = ' '.join((i.strip() for i in title_text.split() if i))

            link = title_tag['href']
            last_segment = link.split('/')[-1]
            vacancy_id = last_segment.split('?')[0]
            
            company_name = ''
            company_tag = vacancy_item.find('a',{'data-qa':'vacancy-serp__vacancy-employer'})
            if company_tag:
                company_text = company_tag.text.strip()
                company_name = ' '.join([i.strip() for i in company_text.split() if i])
            
            vacancy_data = get_vacancy_data(vacancy_id)
            if vacancy_data:
                experience_id = vacancy_data['experience']['id']
                experience = EXPERIENCE_DICTIONARY.get(experience_id)
                description_html = vacancy_data['description']
                soup = BeautifulSoup(description_html,'html.parser')
                description = soup.text
                contact_email = vacancy_data['contacts']['email'] if vacancy_data['contacts'] else None 
                market_ids = [role['id'] for role in vacancy_data['professional_roles']]
                markets = convert_hhmarkets_to_oneappmarkets(market_ids)
                address_tag = vacancy_item.find('div',{'data-qa':'vacancy-serp__vacancy-address'})
                address_text = address_tag.text
                address = ', '.join([address.strip() for address in address_text.split(',')]) 
                skills = [skill['name'] for skill in vacancy_data['key_skills']]
                
                vacancy = {
                    'title': title,
                    'company_name': company_name,
                    'job_location': address,
                    'experience': experience,
                    'markets': list(markets),
                    'contacts': contact_email,
                    'required_skills': skills,
                    'description': description,
                }
                vacancies.append(vacancy)
    else:
        print('Error occured')
    return vacancies
    


RESULT_FILE_NAME = 'scrape_result.json'
def save_vacancies_to_file(vacancies):
    with open(RESULT_FILE_NAME,'w',encoding='utf-8') as f:
        json.dump(vacancies,f,indent=4,ensure_ascii=False)





if __name__ == '__main__':
    vacancies = get_vacancies()
    save_vacancies_to_file(vacancies)













