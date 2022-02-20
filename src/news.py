from bs4 import BeautifulSoup
import requests

def get_soup(link):

    source=requests.get(link).text
    
    return BeautifulSoup(source,'html.parser')


def get_links(soup):
    links = []

    for link in soup.find_all('comments'):
        links.append(link.text[:-9])

    return links


def get_titles(soup):

    title_list = []
    for title in soup.find_all('title')[2:]:
        title_list.append(title.text)
    
    return title_list

def get_news(link):
    soup = get_soup(link)
    
    return get_titles(soup), get_links(soup)

if __name__ == "__main__":
    
    link = 'https://www.infomoney.com.br/feed/'

    soup = get_soup(link)
    titles = get_titles(soup)
    links = get_links(soup)

    titles, links = get_news(link)
    for title, link in zip(titles,links):
        print(f"{title} veja aqui {link} \n")
