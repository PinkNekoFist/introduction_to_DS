import scrapy
from scrapy.selector import Selector

class GetDataMlbSpider(scrapy.Spider):
    name = "get_data_mlb"
    allowed_domains = ["www.mlb.com"]

    def start_requests(self):
        for page in range(1, 5):
            yield scrapy.Request(f"https://www.mlb.com/stats/?page={page}")

    def parse(self, response):
        sel = Selector(response)
        players_list = sel.css(".notranslate > tr")

        for player in players_list:
            first_name =  player.css("th:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > span:nth-child(1)::text").extract_first()
            second_name = player.css("th:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > span:nth-child(3)::text").extract_first()
            player_data = {
                "PLAYER": first_name + " " + second_name,
                "TEAM": player.css("td:nth-child(2)::text").extract_first(),
                "G": player.css("td:nth-child(3)::text").extract_first(),
                "AB": player.css("td:nth-child(4)::text").extract_first(),
                "R": player.css("td:nth-child(5)::text").extract_first(),
                "H": player.css("td:nth-child(6) > a:nth-child(1)::text").extract_first(),
                "2B": player.css("td:nth-child(7) > a:nth-child(1)::text").extract_first(),
                "3B": player.css("td:nth-child(8)::text").extract_first(),
                "HR": player.css("td:nth-child(9) > a:nth-child(1)::text").extract_first(),
                "RBI": player.css("td:nth-child(10)::text").extract_first(),
                "BB": player.css("td:nth-child(11) > a:nth-child(1)::text").extract_first(),
                "SO": player.css("td:nth-child(12) > a:nth-child(1)::text").extract_first(),
                "SB": player.css("td:nth-child(13)::text").extract_first(),
                "CS": player.css("td:nth-child(14)::text").extract_first(),
                "AVG": player.css("td:nth-child(15)::text").extract_first(),
                "OBP": player.css("td:nth-child(16)::text").extract_first(),
                "SLG": player.css("td:nth-child(17)::text").extract_first(),
                "OPS": player.css("td:nth-child(18)::text").extract_first()
            }
            player_data = {k: (v if v is not None else '0') for k, v in player_data.items()}
            yield player_data