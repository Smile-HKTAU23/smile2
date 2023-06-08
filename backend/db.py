from dataclasses import dataclass, asdict
import json


DB_FILENAME = "db.json"

@dataclass
class Location:
    lat: float
    lon: float

@dataclass
class User:
    id: str
    name: str

    dict = asdict

@dataclass()
class Course:
    id: str
    source: Location
    destination: Location

@dataclass
class SmileDB:
    db_filename: str

    def get_section(self, section_name):
        with open(self.db_filename) as f:
            content = f.read()
            data = json.loads(content)
            return data[section_name]

    # def get_users(self):
    #     return self.get_section("users")

    def get_courses(self):
        courses_data = self.get_section("courses")
        courses = [Course(**d) for d in courses_data]
        return courses
