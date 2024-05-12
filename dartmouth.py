"""
Copyright (C) 2024 Daniel Ellison Th '24. All rights reserved. 

Interfaces to the Dartmouth Timetable and API

>>> key = '<...Dartmouth API key...>'
>>> api = API(key)
>>> sections = api.query("academic/sections", "end_date=>2024-04-22T19:04:57Z")
>>> sections[0]
{'id': 'CLSP.031.01-202303-P-32434', 'status_id': 'A', 'name': 'Water Polo Club - Women', 'subject_id': 'CLSP', 'course_number': '031', ...}

>>> timetable = Timetable(terms=['202403'])
>>> vars(timetable.data['<...CRN...>']) 
{'wc': [], 'dist': [], 'lang': None, 'fys': True, 'enrl': 12, 'lim': 16}
"""


from bs4 import BeautifulSoup, Tag
import requests
from requests_html import HTMLSession
from typing import Any

class API:
    def __init__(self, key: str) ->  None:
        self.jwt = self._login(key)

    def _login(self, key: str) -> str:
        response = requests.post("https://api.dartmouth.edu/api/jwt", headers={"Authorization": key})
        response.raise_for_status()
        return response.json()["jwt"]

    def query(self, api: str, params: str = '') -> list[dict[str, Any]]:
        done, continuation_key = False, None
        page, page_size = 1, 1000
        results = []

        while not done:
            if page == 1:
                url = f"https://api.dartmouth.edu/api/{api}?{params}&pagesize={page_size}&page{page}"
            else:
                url = f"https://api.dartmouth.edu/api/{api}?continuation_key={continuation_key}&pagesize={page_size}&page={page}"
            
            response = requests.get(url, headers={"Authorization": f"Bearer {self.jwt}"})
            response.raise_for_status()
            if page == 1:
                continuation_key = response.headers.get("x-request-id")
            response_list = response.json()
            results.extend(response_list)
            page += 1
            
            if len(response_list) == 0:
                done = True

        return results


class TimetableEntry:
    def __init__(self, row: dict[str, Tag]):
        self.wc:   list[str]   = self._clean(row["WC"].getText()).split()
        self.dist: list[str]   = self._clean(row["Dist"].getText()).replace(" or ", ' ').split()
        self.lang: str | None  = self._clean(row["Lang Req"].getText()) if self._clean(row["Lang Req"].getText()) != '' else None
        self.fys:  bool        = True if self._clean(row["FYS"].getText()) == 'Y' else False
        self.enrl: int | None  = int(self._clean(row["Enrl"].getText())) if self._clean(row["Enrl"].getText()).isdigit() else None
        self.lim:  int | None  = int(self._clean(row["Lim"].getText())) if self._clean(row["Lim"].getText()).isdigit() else None
    def _clean(self, txt:str) -> str:
        return txt.replace("&nbsp", '').strip()
    
class Timetable:
    def __init__(self, terms: list[str]) -> None:
        self.data = self._scrape(self._fetch(terms))

    def _fetch(self, terms: list[str]) -> BeautifulSoup:
        if len(terms) == 1:
            terms.append('')
        url = "https://oracle-www.dartmouth.edu/dart/groucho/timetable.display_courses"
        payload = {
            "classyear": "2008",
            "searchtype": "Subject Area(s)",
            "pmode": "public",
            "term": "",
            "levl": "",
            "fys": "n",
            "wrt": "n",
            "pe": "n",
            "review": "n",
            "crnl": "no_value",
            "termradio": "selectterms",
            "terms": terms,
            "hoursradio": "allhours",
            "periods": "no_value",
            "subjectradio": "allsubjects",
            "depts": "no_value",
            "deliveryradio": "alldelivery",
            "deliverymodes": "no_value",
            "distribs_i": "no_value",
            "distribs_wc": "no_value",
            "distribs_lang": "no_value",
            "distribradio": "alldistribs",
            "distribs": "no_value",
            "sortorder": "dept",
        }
        session = HTMLSession()
        response = session.post(url, data=payload)
        response.html.render()
        return BeautifulSoup(response.text, features="lxml")
    
    def _scrape(self, HTML: BeautifulSoup) -> dict[str, TimetableEntry]:
        course_table = HTML.find("div", {"class": "data-table"})
        if isinstance(course_table, Tag):
            table_headers = [th.text for th in course_table.find_all("th")]
            table_entries = iter(course_table.find_all("td"))
            table_rows = zip(*[table_entries] * len(table_headers))
            parsed = {}
            for raw_row in table_rows:
                row = dict(zip(table_headers, raw_row))
                crn = row['Text'].find('a')['href'].rpartition('=')[2][:-2]
                parsed[crn] = TimetableEntry(row)
            return parsed
        else:
            raise Exception("HTML is missing the course table (<div class='data-table'...)")
