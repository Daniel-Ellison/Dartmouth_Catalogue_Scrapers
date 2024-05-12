"""
Copyright (C) 2024 Daniel Ellison Th '24. All rights reserved.

Scrape data from Timetable and API into JS data file

>>> dartmouth_key = "...Dartmouth API key..."
>>> updater = Manager(dartmouth_key)
>>> updater.save("data.js")
"""

import dartmouth
import datetime
import json
from typing import Any

class Manager:
    def __init__(self, dartmouth_key: str) -> None:
        self.API = dartmouth.API(dartmouth_key)

        self.sections = self._get_sections()
        self.courses = self._get_courses()
        self.section_types = self._get_section_types()
        self.people = self._get_people()
        self.timetable = self._get_timetable()
    
    def _get_sections(self) -> dict[str, dict[str, Any]]:
        today = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        sections = self.API.query("academic/sections", f"end_date=>{today}&course_assessment.end_date=>{today}")
        keys = ["course_id", "section_number", "crn", "enroll_limit","priorities", "required_materials", "schedule", "crosslist","term", "type_id", "instructors", "start_date", "end_date"]
        return {section["id"]: {key: section[key] for key in keys} for section in sections}
    
    def _get_courses(self) -> dict[str, dict[str, Any]]:
        courses = self.API.query("academic/courses")
        ids = set(section["course_id"] for section in self.sections.values())
        keys = ["course_number", "subject_id", "name", "orc_title", "orc_description", "prerequisites", "is_credit_nocredit", "schools"]
        return {course["id"]: {key: course[key] for key in keys} for course in courses if course["id"] in ids}
    
    def _get_section_types(self) -> dict[str, str]:
        sec_types = self.API.query("academic/section_types")
        return {sec_type["id"]: sec_type["name"] for sec_type in sec_types}
    
    def _get_people(self) -> dict[str, dict[str, str]]:
        netids = set(sum([[prof["netid"] for prof in section["instructors"]] for section in self.sections.values()], []))
        try:
            people = json.load(open('people.json'))
            if any(netid not in people for netid in netids):
                people = {person["netid"]: person for person in self.API.query("people")}
        except FileNotFoundError:
            people = {person["netid"]: person for person in self.API.query("people")}
        json.dump(people, open("people.json", 'w'))
        keys = ["name", "email"]
        return {netid: {key: person[key] for key in keys} for netid, person in people.items() if netid in netids}

    def _get_timetable(self) -> dict[str, dict[str, Any]]:
        terms = set([section["term"]["sis_term_code"] for section in  self.sections.values()])
        timetable = dartmouth.Timetable(terms=list(terms))
        return {crn: vars(value) for crn, value in timetable.data.items()}

    def save(self, filename: str) -> None:
        with open(filename, 'w') as file:
            file.writelines(["const API = {\n",
                             "\t academic: {\n",
                            f"\t\t sections: {json.dumps(self.sections)},\n",
                            f"\t\t section_types: {json.dumps(self.section_types)},\n",
                            f"\t\t courses: {json.dumps(self.courses)}\n",
                             "\t },\n",
                            f"\t people: {json.dumps(self.people)},\n",
                            f"\t cache_date: '{datetime.datetime.now()}'\n",
                             "};\n",
                            f"const Timetable = {json.dumps(self.timetable)};\n"
                            ])
