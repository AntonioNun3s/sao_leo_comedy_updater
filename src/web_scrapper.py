from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from datetime import datetime
import time
import json

class web_scrapper:

    def start_browser(self):

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        try:
            service = Service(executable_path="sao_leo_comedy_updater/src/geckodriver.exe")
            driver = webdriver.Firefox(options=options, service=service)
            driver.get("https://www.saoleocomedy.com.br/")
        except Exception as e:
            print(f"algo deu errado. erro: {e}")
        time.sleep(3)

        return driver

    def get_information(self, driver):
        html = driver.page_source

        html_bs = BeautifulSoup(html, "html.parser")

        events = html_bs.find("section", id="eventos")
        div = events.find("div", id="lista-eventos")
        participants = div.find_all("div", class_="bg-white p-4 rounded shadow hover:shadow-lg transition-shadow duration-300")

        driver.quit()

        return participants

    def sort_participants(self, participants):

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

            print(info_participant)
            information.append(info_participant)

            print("------------------------------------------------------------------------------------------")
            print()

        return information

    def save_JSON(self, information):
        
        with open("sao_leo_comedy_updater/data/data.json", "w", encoding="utf-8") as file:

            json.dump(information, file, indent=4, ensure_ascii=False)

    