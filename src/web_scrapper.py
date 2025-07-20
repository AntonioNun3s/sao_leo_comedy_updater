from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from datetime import datetime
import time
import json

class web_scrapper:

    # scraps the information of the website

    def start_browser(self):

        # runs it in headless mode to save CPU and RAM
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        try:
            service = Service(executable_path="src/geckodriver.exe")
            driver = webdriver.Firefox(options=options, service=service)
            driver.get("https://www.saoleocomedy.com.br/")
        except Exception as e:
            print(f"algo deu errado. erro: {e}")
        time.sleep(3)

        return driver

    # manages the scrapped info of the site and turns it into an array of the artists

    def get_information(self, driver):
        html = driver.page_source

        html_bs = BeautifulSoup(html, "html.parser")

        events = html_bs.find("section", id="eventos")
        div = events.find("div", id="lista-eventos")
        participants = div.find_all("div", class_="bg-white p-4 rounded shadow hover:shadow-lg transition-shadow duration-300")

        driver.quit()

        return participants

    # filters the participants array into an array of dictionaries

    def filter_participants(self, participants):

        information = []
        today = datetime.today()

        for participant in participants:

            info_participant = {
                "name": "",
                "date": None,
                "days_for_the_show": None
            }

            info = participant.find("p")

            date_n_time_raw = info.find_all(string=True)
            date_n_time_raw[1] = date_n_time_raw[1].strip()
            date_n_time_raw[2] = date_n_time_raw[2].strip()

            title_name = participant.find("h3").find(string=True).replace(" em SÃO LEOPOLDO", "").replace(" m SÃO LEOPOLDO", "").strip()

            date_n_time = datetime.strptime(date_n_time_raw[1] + date_n_time_raw[2], "%d/%m/%Y%H:%M")
            days_for_the_show = date_n_time - today

            info_participant["name"] = title_name
            info_participant["date"] = date_n_time_raw[1]
            info_participant["time"] = date_n_time_raw[2]
            info_participant["days_for_the_show"] = days_for_the_show.days
            information.append(info_participant)

        print(today)
        print("dados pegos com sucesso")

        return information

    # saves the new array of dictionaries on the JSON where the bot later will get and manage it

    def save_JSON(self, information):
        
        with open("data/data.json", "w", encoding="utf-8") as file:

            json.dump(information, file, indent=4, ensure_ascii=False)

    