import scrapy


class GetDataMlbSpider(scrapy.Spider):
    name = "get_data_mlb"
    allowed_domains = ["www.mlb.com"]
    start_urls = ["https://www.mlb.com/stats/"]

    def parse(self, response):
        for player in response.xpath("//tr[@class='p1']"):
            name = player.xpath("td[@class='dg-name_display_first_last']/a/text()").get()
            position = player.xpath("td[@class='dg-position']/text()").get()
            team = player.xpath("td[@class='dg-team_abbrev']/text()").get()
            at_bats = player.xpath("td[@class='dg-ab']/text()").get()
            runs = player.xpath("td[@class='dg-r']/text()").get()
            hits = player.xpath("td[@class='dg-h']/text()").get()
            doubles = player.xpath("td[@class='dg-2b']/text()").get()

            # Print extracted data for debugging
            print(f"Name: {name}, Position: {position}, Team: {team}, At Bats: {at_bats}, Runs: {runs}, Hits: {hits}, Doubles: {doubles}")

            if name and position and team and at_bats and runs and hits and doubles:
                yield {
                    'name': name,
                    'position': position,
                    'team': team,
                    'at_bats': at_bats,
                    'runs': runs,
                    'hits': hits,
                    'doubles': doubles,
                }