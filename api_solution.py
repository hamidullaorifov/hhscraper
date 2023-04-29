from bs4 import BeautifulSoup
import requests
import json
from utils import convert_hhmarkets_to_oneappmarkets,EXPERIENCE_DICTIONARY


API_ROOT_URL = 'https://api.hh.ru/'
VACANCIES_URL = f'{API_ROOT_URL}vacancies/'
PERIOD = 1
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
    response = requests.get(VACANCIES_URL,params={'period':PERIOD},headers=HEADERS)
    if response.status_code == requests.codes.ok:
        data = response.json()
        vacancies = []
        for item in data.get('items',[]):
            title = item.get('name')
            employer = item.get('employer',None)
            company_name = employer.get('name') if employer else ''        
            experience_id = item['experience']['id']
            experience = EXPERIENCE_DICTIONARY.get(experience_id)
            market_ids = [role['id'] for role in item['professional_roles']]
            markets = convert_hhmarkets_to_oneappmarkets(market_ids)   
            address = item.get('address')
            address_text = address.get('raw') if address else item.get('area',{}).get('name')
            vacancy_data = get_vacancy_data(item['id'])
            contact_email = vacancy_data['contacts']['email'] if vacancy_data['contacts'] else None 
            description_html = vacancy_data['description']
            soup = BeautifulSoup(description_html,'html.parser')
            description = soup.text
            skills = [skill['name'] for skill in vacancy_data['key_skills']]
            vacancy = {
                    'title': title,
                    'company_name': company_name,
                    'job_location': address_text,
                    'experience': experience,
                    'markets': list(markets),
                    'contacts': contact_email,
                    'required_skills': skills,
                    'description': description,
                }
            vacancies.append(vacancy)
        return vacancies
    else:
        print('Error occured')
        return []


RESULT_FILE_NAME = 'api_result.json'
def save_vacancies_to_file(vacancies):
    with open(RESULT_FILE_NAME,'w',encoding='utf-8') as f:
        json.dump(vacancies,f,indent=4,ensure_ascii=False)





if __name__ == '__main__':
    vacancies = get_vacancies()
    save_vacancies_to_file(vacancies)











# print(title)
# print(title_text)
# print(link)


# root_url = 'https://tashkent.hh.uz/search/vacancy?'
# market_filters = {
#     'Information Technology(IT)':'professional_role=156&professional_role=160&professional_role=10&professional_role=12&professional_role=150&professional_role=25&professional_role=165&professional_role=34&professional_role=36&professional_role=73&professional_role=155&professional_role=96&professional_role=164&professional_role=104&professional_role=157&professional_role=107&professional_role=112&professional_role=113&professional_role=148&professional_role=114&professional_role=116&professional_role=121&professional_role=124&professional_role=125&professional_role=126',
#     'Software Development':'professional_role=96&professional_role=104&professional_role=124&professional_role=160&professional_role=25&professional_role=165&professional_role=112&professional_role=113',
#     'Management':'professional_role=68&professional_role=76&professional_role=70&professional_role=66&professional_role=73&professional_role=88&professional_role=1&professional_role=2&professional_role=3&professional_role=71&professional_role=75&professional_role=67&professional_role=72&professional_role=74&professional_role=153&professional_role=69&professional_role=158&professional_role=137',
#     'Design':'professional_role=25&professional_role=34&professional_role=12',
#     'Web Development':'professional_role=96',
#     'Education':'professional_role=17&professional_role=23&professional_role=167&professional_role=132&professional_role=79',
#     'Sales':'professional_role=70&professional_role=73&professional_role=97&professional_role=106',
#     'Marketing':'professional_role=37&professional_role=170&professional_role=163&professional_role=68',
#     'Customer Service':'professional_role=70&professional_role=105',
#     'Enterprise Software (ERP, CRM)':'professional_role=156&professional_role=96',
    
# }   
# def search_by_market(market_id):
#     url = 'https://tashkent.hh.uz/search/vacancy?no_magic=true&L_save_area=true&professional_role=156&professional_role=160&professional_role=10&professional_role=12&professional_role=150&professional_role=25&professional_role=165&professional_role=34&professional_role=36&professional_role=73&professional_role=155&professional_role=96&professional_role=164&professional_role=104&professional_role=157&professional_role=107&professional_role=112&professional_role=113&professional_role=148&professional_role=114&professional_role=116&professional_role=121&professional_role=124&professional_role=125&professional_role=126&area=2759'


# import requests
# import json
# url = "https://api.hh.ru/specializations"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#     "Referer": "https://www.google.com/",
#     "Connection": "keep-alive"
# }
# response = requests.get(url, headers=headers)
# if response.status_code == 200:
#     specialties = json.loads(response.text)
#     roles = []
#     for specialty in specialties:
#         for role in specialty['specializations']:
#             roles.append(role['name'])
#     roles = list(set(roles))
#     roles.sort()
#     print(len(roles))
#     with open('roles.txt','w',encoding='utf-8') as f:
#         f.write('\n'.join(roles))
# else:
#     print(f"Error: {response.status_code}")



# import requests
# from pprint import pprint
# url = 'https://api.hh.ru/dictionaries'
# params = {'only_with_vacancies': True}
# response = requests.get(url, params=params)
# data = response.json()
# print(data)
# professional_roles = data.get('specializations')
# if professional_roles:
#     pprint(professional_roles)
# else:
#     print('Error occurred while retrieving professional roles')