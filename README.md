# Dartmouth_Catalogue_Scrapers

Provides data scrapers for Dartmouth College's course offerings. 

## Usage

Visit http://developer.dartmouth.edu to get an API key.
```
>>> import update 
>>> dartmouth_key = "...Dartmouth API key..."
>>> updater = update.Manager(dartmouth_key)
>>> updater.save("data.js")
```

### Data Formatting

Structure of `data.js`
```
const API = {
    academic: {
        sections: {<section_id>: ...},
        section_types: {<section_type>: ...},
        courses: {<course_id>: ...},
    },
    people: {<netid>: ...}
}

const Timetable = {
    <crn>: ...
}
```

#### API.academic.sections (sample)
> Schema is coordinated with the [Dartmouth API](http://developer.dartmouth.edu). 

```
"COSC.030.01-202403-U-30984": {
    "course_id": "COSC.030-201109",
    "section_number": "01",
    "crn": "30984",
    "enroll_limit": 55,
    "priorities": [
        {
            "is_overlaps": true,
            "item_number": 7,
            "major_id": "COSC",
            "school_year": "Junior",
            "set_number": 24847,
            "type": "Majors"
        }, ...
    ],
    "required_materials": "None",
    "schedule": {
        "type_id": "2",
        "sessions": [
            {
                "start_date": "2024-03-25T04:00:00Z",
                "end_date": "2024-06-04T04:00:00Z",
                "local_begin_time": "13:20:00",
                "local_end_time": "14:10:00",
                "class_days": [
                    {
                        "id": "R"
                    }
                ],
                "is_x_session": true,
                "location": {
                    "building": {
                        "code": "CECS",
                        "name": "Engineering & CS Center"
                    },
                    "room": "116"
                }
            }, ...
        ]
    },
    "crosslist": {
        "id": "D5-202403",
        "sections": [
            {
                "id": "COSC.030.01-202403-U-30984"
            },
            {
                "id": "ENGS.066.01-202403-U-31402"
            }
        ]
    },
    "term": {
        "id": "202403-U",
        "lms_term_id": "SP24",
        "sis_term_code": "202403",
        "sis_ptrm_code": "U"
    },
    "type_id": "L",
    "instructors": [
        {
            "netid": "f004t52",
            "is_primary": true
        }
    ],
    "start_date": "2024-03-25T04:00:00Z",
    "end_date": "2024-06-04T04:00:00Z"
}
```

#### API.academic.section_types (sample)
> Schema is coordinated with the [Dartmouth API](http://developer.dartmouth.edu). 
```
"L": "Lecture"
```
#### API.academic.courses (sample)
> Schema is coordinated with the [Dartmouth API](http://developer.dartmouth.edu). 
```
"COSC.030-201109": {
    "course_number": "030",
    "subject_id": "COSC",
    "name": "Discrete Math Computer Sci",
    "orc_title": "NA",
    "orc_description": "NA",
    "prerequisites": "NA",
    "is_credit_nocredit": false,
    "schools": [
        {
            "id": "GR"
        },
        {
            "id": "UG"
        }
    ]
}
```
#### API.people (sample)
> Schema is coordinated with the [Dartmouth API](http://developer.dartmouth.edu). 
```
"f004t52": {
    "name": "Hsien-Chih Chang",
    "email": "Hsien-Chih.Chang@dartmouth.edu"
}
```

#### Timetable (sample)
```
"30984": {
    "wc": [],
    "dist": [
        "QDS"
    ],
    "lang": null,
    "fys": false,
    "enrl": 60,
    "lim": 60
}
```

