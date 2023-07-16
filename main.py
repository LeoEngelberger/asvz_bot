#  Copyright © 2023 Leo Engelberger
#  #
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  #
#      http://www.apache.org/licenses/LICENSE-2.0
#  #
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import http.client
import json

# env vars #
sorted_entries = {}
payload_for_fahrplan = ''
headers_for_fahrplan = {}
lessons_with_name = {}
lessons_of_type = []


# get id from detail view on schalter.asvz.ch exp: https://schalter.asvz.ch/tn/lessons/534848
course_id = "534848"

# get auth token by looking for member_info package under network in the inspector of your browser of choice
# it's the really long encrypted string
authorization_token = \
 "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"


def get_all_lessons():
    conn_to_sportfahrplan = http.client.HTTPSConnection("asvz.ch")
    conn_to_sportfahrplan.request("GET", "/asvz_api/event_search?_format=json&limit=2000", payload_for_fahrplan,
                                  headers_for_fahrplan)
    res_sportfahrplan = conn_to_sportfahrplan.getresponse()
    sportfahrplan_data = res_sportfahrplan.read()
    parsed_data = json.loads(sportfahrplan_data)
    entries = parsed_data['results']
    # Create a dictionary to store the filtered and sorted entries

    # Loop through the entries
    for entry in entries:
        sport_name = entry['sport_name']
        # Check if the sport_name already exists as a key in the dictionary
        if sport_name in sorted_entries:
            # If it does, append the entry to the existing list of entries
            sorted_entries[sport_name].append(entry)
        else:
            # If it doesn't, create a new list with the entry as the first element
            sorted_entries[sport_name] = [entry]


def find_all_lessons_with_name(name):
    global lessons_with_name
    all_lessons_with_name = None
    for entry in sorted_entries:
        if entry == name:
            all_lessons_with_name = sorted_entries[entry]
    lessons_with_name = all_lessons_with_name


def find_lessons_of_type():
    global lessons_of_type
    for lesson in lessons_with_name:
        print(lesson['title'])
        if lesson['title'] == "Akrobatik":
            lessons_of_type.append(lesson)


def enroll_in_lesson():
    conn = http.client.HTTPSConnection("schalter.asvz.ch")
    payload = '_format=json&limit=60'
    headers = {
        'Authorization': f'Bearer {authorization_token}'
    }

    url = "/tn-api/api/Lessons/%s/Enrollment" % course_id
    print(url)
    conn.request("POST", url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


get_all_lessons()
find_all_lessons_with_name("Manege")
find_lessons_of_type()
print(sorted_entries)
