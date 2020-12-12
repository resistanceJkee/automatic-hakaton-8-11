import json
import os
import io
import time
from transliterate import translit
import cherrypy
import configparser as cp
import requests as req
from bs4 import BeautifulSoup
from pdfminer.converter import *
from pdfminer.pdfinterp import *
from pdfminer.pdfpage import *
from selenium.webdriver.firefox.options import *
from selenium import webdriver
from fpdf import FPDF


class CommandA(object):
    iata = []
    from_city = ""
    to_city = ""
    prices_avia = {}
    prices_hotel = {}

    @cherrypy.expose
    def index(self):
        """
        Редиректер со страницы index на страницу static
        :return:
        """
        raise cherrypy.HTTPRedirect("/static/")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_ret_inf(self, **data):
        """
        Основная функция бэкэнда, которая получает в себя дату через getJSON. Далее
        производится поочередной вызов функций, которые должны получить информацию об авиабилетах,
        отелях и отправить их обратно на фронт
        :param data: словарь с 4 парами ключ-значение
        :return:
        """
        print(f'Получены данные {data}')
        start = time.time()
        self.get_codes()
        tickets = self.get_tickets(data["cityIn"], data["cityOut"],
                                   data["dateIn"], data["dateOut"])
        hostels = self.get_prices_hotel(data["cityOut"], data["dateIn"], data["dateOut"])
        self.form_pdf(tickets, hostels)
        print("Ожидание нового запроса...")
        end = time.time()
        print(f'Время работы: {end - start}')
        return json.dumps({"tickets": tickets, "hostels": hostels})

    @staticmethod
    def form_pdf(tickets, hostels):
        """

        :param tickets: билеты
        :param hostels: отели
        :return:
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        flag = False
        try:
            print(tickets[0])
            print(hostels[0])
        except Exception as e:
            flag = True
        if flag:
            try:
                try:
                    flot = translit(tickets["aeroflot"], reversed=True)
                except Exception as e:
                    flot = tickets["aeroflot"]
                baggage = translit(tickets["baggage"], reversed=True)
                date_incoming = translit(tickets["date_in"], reversed=True)
                date_outcoming = translit(tickets["date_return"], reversed=True)
                hostel_name = ""
                try:
                    hostel_name = translit(hostels["hotel"], reversed=True)
                except Exception as e:
                    hostel_name = hostels["hotel"]
                hostel_price = hostels["price"]
                pdf.cell(200, 10, txt="Bilet na samolet", ln=1)
                pdf.cell(200, 10, txt=f'Aviakompaniya: {flot}', ln=1)
                pdf.cell(200, 10, txt=f'Price: {tickets["price"]}', ln=1)
                pdf.cell(200, 10, txt=f'Bagaj: {baggage}', ln=1)
                pdf.cell(200, 10, txt=f'Data vileta: {date_incoming}', ln=1)
                pdf.cell(200, 10, txt=f'Data na samolet obratno: {date_outcoming}', ln=1)
                pdf.cell(200, 10, txt=f'-------------------------------------------------------', ln=1)
                pdf.cell(200, 10, txt=f'Tsena na hostel', ln=1)
                pdf.cell(200, 10, txt=f'Nazvanie: {hostel_name}, tsena: {hostel_price}', ln=1)
                pdf.cell(200, 10, txt=f'-------------------------------------------------------', ln=1)
                pdf.cell(200, 10, txt=f'Obshaya tsena: {round(tickets["price"] + hostel_price, 2)}', ln=1)
                pdf.output("./static/inf.pdf")
            except Exception as e:
                print(f"В блоке except")
            finally:
                pdf.cell(200, 10, txt=f'Oshibki sluchautsya... :(', ln=1)
                pdf.output("./static/inf.pdf")
        else:
            pdf.cell(200, 10, txt="Nothing...", ln=1)
            pdf.output("./static/inf.pdf")

    def get_tickets(self, from_city, to_city, date_in, date_out):
        """
        Получение данных о билетах на указанную дату и город. Сначала происходит
        получение IATA кодов города, затем преобразовывается дата, чтобы можно было
        вставить всё в ссылку, которая потом в запросе вернула бы ответ вебдрайверу.
        Вебдрайвер представляет собой GUIless браузер Firefox (драйвер gecko), который
        выполняет запрос к сайту и там прогружает виртуальное DOM дерево. Чтобы его получить
        необходимо подождать примерно 12 секунд (но с запасом поставлено 15). Далее происходит
        вызов функции, которая парсит страницу и возвращает всё в виде листа словарей. После
        рассматриваются варианты того, что вернулся 1+ результат, тогда выбирается самый
        минимальный и ретёрнится или же вернётся nothing, если билеты не были найдены
        :param from_city:
        :param to_city:
        :param date_in:
        :param date_out:
        :return:
        """
        print("Получение IATA кодов")
        code_in = self.get_code_by_city(from_city)
        code_out = self.get_code_by_city(to_city)
        if code_out is None or code_in is None:
            data = ["nothing"]
            return data[0]
        print("Преобразовывание даты в формат МЕСЯЦДЕНЬ")
        from_date = date_in[8] + date_in[9] + date_in[5] + date_in[6]
        to_date = date_out[8] + date_out[9] + date_out[5] + date_out[6]
        link = f'https://www.aviasales.ru/search/{code_in}{from_date}{code_out}{to_date}1'
        print("Настройка драйвера")
        opts = Options()
        opts.set_headless()
        assert opts.headless
        print("Ожидание включения драйвера")
        browser = webdriver.Firefox(options=opts)
        for i in range(5):
            time.sleep(1)
            print(i+1, end=" ")
        print("")
        print("Ожидание прогрузки страницы")
        browser.get(link)
        for i in range(15):
            time.sleep(1)
            print(i+1, end=" ")
        print("")
        btn = browser.find_element_by_class_name("_button_button_lmpwR")
        webdriver.ActionChains(browser).click(btn)
        price_ticket = browser.find_elements_by_class_name("ticket-desktop")
        data = self.parse_ticket(price_ticket)
        browser.close()
        if len(data) == 0:
            data.append("nothing")
            print("Нет билетов")
        else:
            data_sort = []
            j = 0
            for item in data:
                if "Аэрофлот" in item["aeroflot"]:
                    data_sort.append(item)
                    j += 1
            data_out = []
            if len(data_sort) >= 1:
                print("Нашёлся Аэрофлот")
                for clock in data_sort:
                    if int(clock["date_in"].split(" ")[0].split(":")[0]) >= 18:
                        data_out.append(clock)
                if len(data_out) >= 1:
                    return data_out[0]
                data_sort.sort(key=lambda x: x["price"])
                return data_sort[0]
            else:
                k = 0
                for clock in data:
                    if int(clock["date_in"].split(" ")[0].split(":")[0]) >= 18:
                        data_out.append(clock)
                        k += 1
                if k == 0:
                    data.sort(key=lambda x: x["price"])
                    return data[0]
                elif k >= 1:
                    data_out.sort(key=lambda x: x["price"])
                    return data_out[0]
                return data_out[0]
        return data[0]

    def parse_ticket(self, elements):
        """
        Здесь происходит парсинг страницы по классам. В segment-route__time есть 4 даты (то есть существует
        таких 4 класса), каждый нечётный элемент означает время взлёта самолёта. Также может
        быть 2 авиакомпании: одна доставляет из А в Б, вторая из Б в А, поэтому поставлено
        дополнительное условие для обыгрывания такого момента
        :param elements: список всех найденых родительских элементов
        :return:
        """
        data = []
        for each_elem in elements:
            aeroflot = each_elem.find_elements_by_class_name("ticket-carrier__img")
            price = each_elem.find_element_by_class_name("buy-button__price").text
            baggage = each_elem.find_element_by_class_name("ticket-tariffs__title").text
            dates = each_elem.find_elements_by_class_name("segment-route__date")
            dict_date_in = ""
            dict_date_out = ""
            for i, clock in enumerate(each_elem.find_elements_by_class_name("segment-route__time")):
                if i == 0:
                    dict_date_in = clock.text + " " + dates[i].text
                elif i == 2:
                    dict_date_out = clock.text + " " + dates[i].text
                    break
            if len(aeroflot) == 1:
                aeroflot = aeroflot[0].get_attribute("alt")
            else:
                aeroflot = aeroflot[0].get_attribute("alt") + "/" + aeroflot[1].get_attribute("alt")
            price = self.delete_space(price)
            data.append({"aeroflot": aeroflot, "price": price,
                         "baggage": baggage, "date_in": dict_date_in,
                         "date_return": dict_date_out})
        return data

    @staticmethod
    def delete_space(word):
        """
        Валидирует полученную цену за билет. Изначально приходит с юникод-пробелами и
        символом рубля. Чтобы можно было легко преобразовать в int/float происходит удаление
        пробелов и знака рубля. Сначала оно разбивается на лист, затем в цикле удаляются все
        ненужные символы и после через join собирается в одну строку и возвращается int
        :param word:
        :return:
        """
        word = list(word)
        i = 0
        while i < len(word):
            if word[i] == u'\u2009' or word[i] == "₽":
                word.pop(i)
                i -= 1
            i += 1
        word = "".join(word)
        return int(word)

    def get_codes(self):
        """
        Получает IATA коды из файла iata2.json
        :return:
        """
        if os.path.exists("iata2.json"):
            with open("iata2.json", "r", encoding="utf-8") as f:
                self.iata = json.load(f)

    def get_prices_hotel(self, city_out, date_in, date_out):
        """
        Функция выполняет поиск данных обо всех отелях в данном городе
        за текущий период времени. Формируется ссылка с параметрами даты и города,
        затем происходит запрос, который возвращает json объект, впоследствии который
        в цикле обходится и все данные добавляются в лист, в формате словаря
        :param city_out: город, в который летим
        :param date_in: дата заселения
        :param date_out: дата выселения
        :return:
        """
        data = []
        query = f"http://engine.hotellook.com/api/v2/cache.json?location={city_out}" \
                f"&currency=rub&checkIn={date_in}&checkOut={date_out}&limit=10"
        self.prices_hotel = req.get(query).json()
        for i in range(len(self.prices_hotel)):
            try:
                data.append({"hotel": self.prices_hotel[i]["hotelName"], "price": self.prices_hotel[i]["priceFrom"]})
            except Exception as e:
                break
        if len(data) == 0:
            print("Нет данных об отелях")
            data.append("nothing")
        else:
            print("Получены данные об отелях")
            data.sort(key=lambda item: item["price"])
        return data[0]

    def get_code_by_city(self, city):
        """
        Поиск IATA кода по городу
        :param city:
        :return:
        """
        for i in range(len(self.iata)):
            k = list(self.iata[i].keys())[0]
            if k.find(city) != -1:
                print(self.iata[i][k])
                return self.iata[i][k]


def main(config_file="settings.ini"):
    ca = CommandA()
    config = cp.ConfigParser()
    config.read(config_file)
    cherrypy.quickstart(CommandA(), "/", {
        "global": {
            "server.socket_host": config["Server"]["host"],
            "server.socket_port": int(config["Server"]["port"]),
            "tools.staticdir.root": config["Path"]["static_dir"]
        },
        "/static": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "static",
            "tools.staticdir.index": "index.html"
        }
    })


if __name__ == '__main__':
    main()
