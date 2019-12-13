from os import path

BASE_DIR = path.dirname(path.realpath(__file__))
REQUEST_HEADER = 'Web-scraping project (bolotnikovprojects@gmail.com)'

DIVIDERS = ['-', '–', '—']

LINKS = (
         'https://www.work.ua', # 0 Parsing
         'https://rabota.ua', # 1 API
         'https://www.linkedin.com', # 2 API
         'https://hh.ua', # 3 API
         'https://jobs.ua', # 4 Paarsing
         'https://ua.jooble.org', # 5 Parsing
         'http://www.trud.ua', # 6 Parsing
         'https://jobis.com.ua', # 7 Parsing
         'http://novarobota.ua', # 8 Parsing
        )

RABOTAUA_BASELINK = 'https://rabota.ua'
# TODO: Use site's API
RABOTAUA_LINK = 'https://rabota.ua/jobsearch/vacancy_list?keyWords='
RABOTAUA_FILE = BASE_DIR + '/json/jobs_list__rabota_ua.json'
RABOTAUA_CITIES = {
    'Киев': '&regionId=1',
    'Одесса': '&regionId=3',
    'Днепр': '&regionId=4',
    # 'Харьков': '&regionId=0',
    'Львов': '&regionId=2'
}

WORKUA_BASELINK = 'https://www.work.ua'
WORKUA_LINK = 'https://www.work.ua/ru/jobs-'
WORKUA_FILE = BASE_DIR + '/json/jobs_list__work_ua.json'
WORKUA_CITIES = {
    'Киев': 'kyiv',
    'Одесса': 'odesa',
    'Днепр': 'dnipro',
    'Харьков': 'kharkiv',
    'Львов': 'lviv'
}

JOBSUA_BASELINK = 'https://jobs.ua'
JOBSUA_LINK = 'https://jobs.ua/rus/vacancy/'
JOBSUA_FILE = BASE_DIR + '/json/jobs_list__jobs_ua.json'
JOBSUA_CITIES = {
    'Киев': 'kiev',
    'Одесса': 'odessa',
    'Днепр': 'dnepr',
    'Харьков': 'kharkov',
    'Львов': 'lvov'
}

JOOBLEORG_BASELINK = 'https://ua.jooble.org'
JOOBLEORG_LINK = 'https://ua.jooble.org/%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0/'
JOOBLEORG_FILE = BASE_DIR + '/json/jobs_list__jooble_org.json'
JOOBLEORG_CITIES = {
    'Киев': '%D0%9A%D0%B8%D0%B5%D0%B2',
    'Одесса': '%D0%9E%D0%B4%D0%B5%D1%81%D1%81%D0%B0',
    'Днепр': '%D0%94%D0%BD%D0%B5%D0%BF%D1%80',
    'Харьков': '%D0%A5%D0%B0%D1%80%D1%8C%D0%BA%D0%BE%D0%B2',
    'Львов': '%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2'
}

JOBISCOMUA_BASELINK = 'https://jobis.com.ua'
JOBISCOMUA_LINK = 'https://jobis.com.ua/jobs-city-'
JOBISCOMUA_FILE = BASE_DIR + '/json/jobs_list__jobis_com_ua.json'
JOBISCOMUA_CITIES = {
    'Киев': 'kiev',
    'Одесса': 'odessa',
    'Днепр': 'dnepr',
    'Харьков': 'kharkov',
    'Львов': 'lvov'
}
JOBISCOMUA_CATEGORIES = (
    '/it',
    '/administration',
    '/accounting',
    '/hotel-restaurant-tourism',
    '/design-art',
    '/beauty-sports',
    '/culture-music-showbiz',
    '/logistic-supply-chain',
    '/marketing-advertising-pr',
    '/healthcare',
    '/real-estate',
    '/education-scientific',
    '/security',
    '/sales',
    '/production-engineering',
    '/retail',
    '/office-secretarial',
    '/agriculture',
    '/publishing-media',
    '/insurance',
    '/construction-architecture',
    '/customer-service',
    '/telecommunications',
    '/management-executive',
    '/auto-transport',
    '/hr-recruitment',
    '/banking-finance',
    '/legal',
    '/uncategorized',
    '/management',
    '/office-staff',
    '/students',
    '/home',
    '/migrants'
)

NOVAROBOTAUA_BASELINK = 'http://novarobota.ua'
NOVAROBOTAUA_LINK = 'https://novarobota.ua/city/'
NOVAROBOTAUA_FILE = BASE_DIR + '/json/jobs_list__novarobota_ua.json'
NOVAROBOTAUA_CITIES = {
    'Киев': 'kiev',
    'Одесса': 'odessa',
    'Днепр': 'dnepr',
    'Харьков': 'kharkov',
    'Львов': 'lvov'
}

TRUDUA_BASELINK = 'http://www.trud.ua'
TRUDUA_LINK = 'https://trud.ua/state/'
TRUDUA_FILE = BASE_DIR + '/json/jobs_list__trud_ua.json'
TRUDUA_CITIES = {
    'Киев': 'kiev',
    'Одесса': 'odessa',
    'Днепр': 'dnepr',
    'Харьков': 'kharkov',
    'Львов': 'lvov'
}

PS_STORE_BASELINK = 'https://store.playstation.com'
PS_STORE_LINK = 'https://store.playstation.com/ru-ua/grid/search-игра/'
PS_STORE_DISCOUNT_LINK = 'https://store.playstation.com/ru-ua/grid/STORE-MSF75508-PRICEDROPSCHI/'
PS_STORE_INIT_LINK = 'https://store.playstation.com/ru-ua/grid/STORE-MSF75508-FULLGAMES/'
PS_STORE_FILE = BASE_DIR + '/json/games_list__ps_store_ua.json'
FREE = ['Бесплатно', 'Free']
TITLE_QUERY = 'query='
PRICE_QUERY = 'price='
