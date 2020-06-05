import requests, csv, time
from bs4 import BeautifulSoup
start_url = 'https://www.hse.ru/org/persons/?ltr=%D0%90;udept=22726'


def get_page(url):
    r = requests.get(url)
    return r.text


def get_letter_links():
    letter_list = []
    page = get_page(start_url)
    soup = BeautifulSoup(page)
    links = soup.find('div', {'class':'abc-filter'})
    for link in links.find_all('a'):
        s = 'https://www.hse.ru/org/persons/' + link.get('href')
        letter_list.append(s)
    return letter_list[10:11]


def get_people_links(letter_link):
    people_list = []
    letter_page = get_page(letter_link)
    soup = BeautifulSoup(letter_page)
    soup = soup.find_all('div', {'class': 'post person'})
    for chicken in soup:
        chicken = chicken.find_all('a', {'class': 'link link_dark large b'})
        for egg in chicken:
            s = 'https://www.hse.ru/' + egg.get('href')
            people_list.append(s)
    return people_list


def if_nothing(part_of_page):
    if part_of_page:
        part_of_page = part_of_page.get_text('&')
    else:
        part_of_page = ''
    return part_of_page


def get_personal(people_link):
    person_page = BeautifulSoup(get_page(people_link))
    person_page = person_page.find('div', {'class':'main__inner'})

    name = person_page.find('h1').text
    place = if_nothing(person_page.find('ul', {'class': 'g-ul g-list small'}))
    started_worked = if_nothing(person_page.find('ul', {'class': 'g-ul g-list small person-employment-addition'}))
    education = if_nothing(person_page.find('div', {'tab-node': 'sci-degrees1'}))

    return name, education, place, started_worked


def get_table(letter_link):
    people_links = get_people_links(letter_link)

    with open('big_table.csv', 'a') as csvfile:
        fieldnames = ['name', 'education', 'place', 'started_worked']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for link in people_links:
            personal = get_personal(link)
#             print(personal)
            writer.writerow({'name': personal[0], 'education': personal[1], 'place': personal[2], 'started_worked': personal[3]})


def get_big_table():
    for letter_link in get_letter_links():
        get_table(letter_link)


def main():
    get_big_table()

if __name__ == '__main__':
    main()
