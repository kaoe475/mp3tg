def pars_sound():
    from bs4 import BeautifulSoup
    import requests

    url = 'https://www.myinstants.com/en/categories/memes/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    data = soup.find_all("div", class_="instant")
    list_mus = []

    for i in data:
        b = i.find("button", class_="small-button")
        mus = b.get("onclick")
        url_mus = mus[mus.find("/"):mus.rfind(".mp3")+4]
        list_mus.append(url_mus)
    from random import randint
    return 'https://www.myinstants.com' + list_mus[randint(0, len(list_mus))]


def rand_nick():
    list_nick =['гей','лох','жмот', 'тубуретка', 'элюзианист', 'американ гёрл', 'крутой', 'кам хер', 'лучший','меткий глаз', 'француз', 'негр','любитель жаренных яичек','теплая булочка','сладкий','фонтанчик','калоед','картошка','тепленький','задира','нажимная плита','гонщик по туалетам','инвалид','актер высшего уровня','фокусник с птичкой','яичко','лысый','маринад','макака','рисунок писи','ганстер на горшке','раб','пробирка?','мачо',]
    from random import randint
    return list_nick[randint(0, len(list_nick))]

