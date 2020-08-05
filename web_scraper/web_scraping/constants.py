from os import path

BASE_DIR = path.dirname(path.realpath(__file__))
REQUEST_HEADER = "SCRPR/1.0 (bolotnikovprojects@gmail.com)"

DIVIDERS = ["-", "–", "—"]

LINKS = (
    "https://www.work.ua",  # 0 Parsing
    "https://rabota.ua",  # 1 API
    "https://www.linkedin.com",  # 2 API
    "https://hh.ua",  # 3 API
    "https://jobs.ua",  # 4 Paarsing
    "https://ua.jooble.org",  # 5 Parsing
    "http://www.trud.ua",  # 6 Parsing
    "https://jobis.com.ua",  # 7 Parsing
    "http://novarobota.ua",  # 8 Parsing
)

RABOTAUA_BASELINK = "https://rabota.ua"
RABOTAUA_LINK = "https://rabota.ua/jobsearch/vacancy_list"
RABOTAUA_CITIES = {
    None: "",
    "Киев": "regionId=1&",
    "Одесса": "regionId=3&",
    "Днепр": "regionId=4&",
    "Харьков": "&regionId=21&",
    "Львов": "&regionId=2&",
}

RABOTAUA_API_LINK = "https://api.rabota.ua/vacancy/search"
RABOTAUA_API_CITIES = {
    None: "",
    "Киев": "cityId=1&",
    "Одесса": "cityId=3&",
    "Днепр": "cityId=4&",
    "Харьков": "&cityId=21&",
    "Львов": "&cityId=2&",
}

WORKUA_BASELINK = "https://www.work.ua"
WORKUA_LINK = "https://www.work.ua/ru/jobs-"
WORKUA_CITIES = {
    None: "",
    "Киев": "kyiv",
    "Одесса": "odesa",
    "Днепр": "dnipro",
    "Харьков": "kharkiv",
    "Львов": "lviv",
}

JOBSUA_BASELINK = "https://jobs.ua"
JOBSUA_LINK = "https://jobs.ua/rus/vacancy"
JOBSUA_CITIES = {
    None: "",
    "Киев": "kiev",
    "Одесса": "odessa",
    "Днепр": "dnepr",
    "Харьков": "kharkov",
    "Львов": "lvov",
}

JOOBLEORG_BASELINK = "https://ua.jooble.org"
JOOBLEORG_LINK = "https://ua.jooble.org"
JOOBLEORG_CITIES = {
    None: "",
    "Киев": "%D0%9A%D0%B8%D0%B5%D0%B2",
    "Одесса": "%D0%9E%D0%B4%D0%B5%D1%81%D1%81%D0%B0",
    "Днепр": "%D0%94%D0%BD%D0%B5%D0%BF%D1%80",
    "Харьков": "%D0%A5%D0%B0%D1%80%D1%8C%D0%BA%D0%BE%D0%B2",
    "Львов": "%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2",
}

JOBISCOMUA_BASELINK = "https://jobis.com.ua"
JOBISCOMUA_LINK = "https://jobis.com.ua/jobs-city-"
JOBISCOMUA_CITIES = {
    None: "",
    "Киев": "kiev",
    "Одесса": "odessa",
    "Днепр": "dnepr",
    "Харьков": "kharkov",
    "Львов": "lvov",
}
JOBISCOMUA_CATEGORIES = (
    "/it",
    "/administration",
    "/accounting",
    "/hotel-restaurant-tourism",
    "/design-art",
    "/beauty-sports",
    "/culture-music-showbiz",
    "/logistic-supply-chain",
    "/marketing-advertising-pr",
    "/healthcare",
    "/real-estate",
    "/education-scientific",
    "/security",
    "/sales",
    "/production-engineering",
    "/retail",
    "/office-secretarial",
    "/agriculture",
    "/publishing-media",
    "/insurance",
    "/construction-architecture",
    "/customer-service",
    "/telecommunications",
    "/management-executive",
    "/auto-transport",
    "/hr-recruitment",
    "/banking-finance",
    "/legal",
    "/uncategorized",
    "/management",
    "/office-staff",
    "/students",
    "/home",
    "/migrants",
)

NOVAROBOTAUA_BASELINK = "http://novarobota.ua"
NOVAROBOTAUA_LINK = "https://novarobota.ua/zapros"
NOVAROBOTAUA_CITIES = {
    None: "",
    "Киев": "kiev",
    "Одесса": "odessa",
    "Днепр": "dnepr",
    "Харьков": "kharkov",
    "Львов": "lvov",
}

TRUDUA_BASELINK = "http://www.trud.ua"
TRUDUA_LINK = "https://trud.ua/jobs/list/filter_show/state/q"
TRUDUA_LINK_CITY = "https://trud.ua/state"
TRUDUA_CITIES = {
    None: "",
    "Киев": "kiev",
    "Одесса": "odessa",
    "Днепр": "dnepr",
    "Харьков": "kharkov",
    "Львов": "lvov",
}

HEADHUNTER_BASELINK = "https://hh.ua"
HEADHUNTER_API_LINK = "https://api.hh.ru/vacancies"
HEADHUNTER_LINK = "https://hh.ua/vacancy/"
HEADHUNTER_API_CITIES = {
    None: "area=5&",
    "Киев": "area=115&",
    "Одесса": "area=127&",
    "Днепр": "area=117&",
    "Харьков": "area=135&",
    "Львов": "area=125&",
}

PS_STORE_BASELINK = "https://store.playstation.com"
PS_STORE_LINK = "https://store.playstation.com/ru-ua/grid/search-игра/"
PS_STORE_DISCOUNT_LINK = (
    "https://store.playstation.com/ru-ua/grid/STORE-MSF75508-PRICEDROPSCHI/"
)
PS_STORE_INIT_LINK = (
    "https://store.playstation.com/ru-ua/grid/STORE-MSF75508-FULLGAMES/"
)
PS_STORE_PSPLUS_GAMES = [
    "https://store.playstation.com/ru-ua/grid/STORE-MSF75508-MEMBERSV2/",
    "https://store.playstation.com/ru-ua/grid/STORE-MSF75508-PLUSINSTANTGAME/",
    "https://store.playstation.com/ru-ua/grid/STORE-MSF75508-PLUSEXCLUSIVES/",
]
PS_STORE_FILE = BASE_DIR + "/json/games_list__ps_store_ua.json"
FREE = ["Бесплатно", "Free"]
GAMES_PER_PAGE = 30
