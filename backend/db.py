from dataclasses import dataclass, asdict
import json

DB_FILENAME = "db.json"

@dataclass
class Location:
    lat: float
    lng: float

@dataclass
class LocationWithName:
    lat: float
    lng: float
    name: str

@dataclass
class User:
    id: str
    name: str

    dict = asdict

@dataclass()
class Course:
    id: str
    current_location: Location
    source: LocationWithName
    destination: LocationWithName

@dataclass
class SmileDB:
    db_filename: str

    def get_section(self, section_name):
        with open(self.db_filename) as f:
            content = f.read()
            data = json.loads(content)
            return data[section_name]

    def get_courses(self):
        courses_data = self.get_section("courses")
        return courses_data
