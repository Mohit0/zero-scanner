import requests    
import re    
from urllib.parse import urlparse 
import sys   

class PyCrawler(object):    
    def __init__(self, starting_url):    
        self.starting_url = starting_url    
        self.visited = set()    

    def get_html(self, url):    
        try:    
            html = requests.get(url)    
        except Exception as e:    
            print(e)    
            return ""    
        return html.content.decode('latin-1')    

    def get_links(self, url):    
        html = self.get_html(url)    
        parsed = urlparse(url)    
        base = f"{parsed.scheme}://{parsed.netloc}"    
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)    
        for i, link in enumerate(links):    
            if not urlparse(link).netloc:    
                link_with_base = base + link    
                links[i] = link_with_base    

        return set(filter(lambda x: 'mailto' not in x, links))    

    def extract_info(self, url):    
        html = self.get_html(url)    
        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>", html)    
        return dict(meta)    

    def crawl(self, url):    
        for link in self.get_links(url):    
            if link in self.visited:    
                continue
            elif not(domain) in url:    
                continue 
            self.visited.add(link)    
            info = self.extract_info(link)    

#           print(f"""Link: {link}""")    
#Description: {info.get('description')}    
#Keywords: {info.get('keywords')}    
#            """)    


            print(link)
            f.write(link)
            f.write("\n")   

            self.crawl(link)    

    def start(self):    
        self.crawl(self.starting_url)    

if __name__ == "__main__":
    domain = sys.argv[1]    
    #domain = "hacker.com" 
    protocol = "https://"
    crawl = protocol + domain
    crawler = PyCrawler(crawl)
    path = "output/" + domain
    f=open(path, "a+")
    print("Scanning pages for "+ crawl + " and storing in\t" + path)
    crawler.start()

