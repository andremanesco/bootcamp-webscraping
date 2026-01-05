import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class PadoDeAcucarScraper:
    
    def __init__(self):
        self.origin = "https://www.paodeacucar.com.br/"
        self.products = []
        self.api_key = "paodeacucar"
        self.page = 1
        self.results_per_page = 100
        self.terms = ""
        self.http = self._configure_session()

    def start(self, terms):
        self.terms = terms
        content = self.search_products()
        return self.get_product_data(content)

    def _configure_session(self):
        retry_strategy = Retry(
            total=3,
            status_forcelist=[403, 429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def search_products(self):
        url = "https://api.vendas.gpa.digital/pa/search/search"

        payload = {
            "terms": self.terms,
            "page": self.page,
            "sortBy": "relevance",
            "resultsPerPage": self.results_per_page,
            "allowRedirect": True,
            "storeId": 461,
            "department": "ecom",
            "customerPlus": True,
            "partner": "linx",
            "userHash": "fdcf23d14bb0eafd9f57ef1702499ff22de9530e4f5430383293940cf751acfe"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        try:
            content = self.http.post(url, headers=headers, json=payload)
            if content.status_code == 200:
                return content.json()
            else:
                raise("Error: Status code {}".format(content.status_code))
        except:
            raise(content.status_code)
        
    def get_product_data(self, content):
        if content:
            products = content["products"]
            return products
        else:
            return []
        
terms = "sabonete"
scraper = PadoDeAcucarScraper()
data = scraper.start(terms)
print(data)