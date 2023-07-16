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
from datetime import datetime, timezone, timedelta

# config
with open('config.json') as config_file:
    config_data = json.load(config_file)

relevant_days = config_data["relevant_days"]
type_matter = config_data["type_matter"]
type_name = config_data["type_name"]
course_name = config_data["course_name"]
location_matter = config_data["location_matter"]
locations = config_data["locations"]
authorization_token = config_data["token"]


def convert_time(from_date):
    date_str = from_date
    comprehensive_from_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    your_timezone_offset = timedelta(hours=2)
    your_timezone = timezone(your_timezone_offset)

    # Calculate the time difference between UTC and your local time zone
    time_difference = comprehensive_from_date.replace(tzinfo=timezone.utc) - comprehensive_from_date.replace(
        tzinfo=your_timezone)

    # Convert the datetime object to your local time zone
    localized_from_date = comprehensive_from_date + time_difference
    return localized_from_date.strftime('%Y-%m-%d %H:%M:%S %Z')


def get_course_id(lesson):
    lesson_url = lesson['url']
    split_url = lesson_url.split('/')
    return split_url[-1]


def print_lesson_information(lesson):
    print("Name: " + lesson['sport_name'] + "|| Date: " + convert_time(lesson['from_date']) + "|| Location: " + lesson[
        'location'])


def print_lessons_enrolling_to(relevant_lessons):
    for lesson in relevant_lessons:
        print("Name: " + lesson['sport_name'] + "|| Date & Start Time: " + convert_time(
            lesson['from_date']) + "|| Location: " + lesson['location'])


def confirm_enrollment_in_all():
    while True:
        user_input = input("Do you want to enroll in all classes? (y/yes or n/no): ").strip().lower()
        if user_input == 'y' or user_input == 'yes':
            return True
        elif user_input == 'n' or user_input == 'no':
            return False
        else:
            print(
                "Invalid input. Please enter 'y' or 'yes' to enroll in all classes, or 'n' or 'no' to enroll in individual classes.")


def confirm_enrollment_in_single_lesson(relevant_lesson):
    while True:
        user_input = input("Do you want to enroll in this class (y/yes or n/no): ").strip().lower()
        if user_input == 'y' or user_input == 'yes':
            return True
        elif user_input == 'n' or user_input == 'no':
            return False
        else:
            print(
                "Invalid input. Please enter 'y' or 'yes' to enroll in all classes, or 'n' or 'no' to enroll in individual classes.")


def get_all_lessons():
    payload_for_fahrplan = ''
    headers_for_fahrplan = {}
    sorted_entries = {}
    conn_to_sportfahrplan = http.client.HTTPSConnection("asvz.ch")
    conn_to_sportfahrplan.request("GET", "/asvz_api/event_search?_format=json&limit=50", payload_for_fahrplan,
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
    return sorted_entries


def enrol_in_lesson(course_id):
    conn = http.client.HTTPSConnection("schalter.asvz.ch")
    payload = '_format=json&limit=60'
    headers = {'Authorization': authorization_token}

    url = "/tn-api/api/Lessons/%s/Enrollment" % course_id
    conn.request("POST", url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    data.decode("utf-8")


def find_all_lessons_with_name(sorted_entries):
    for entry in sorted_entries:
        if entry == course_name:
            return sorted_entries[entry]


def filter_lessons_by_type(lessons_with_name):
    lessons_of_type = []
    for lesson in lessons_with_name:
        if lesson['title'] == type_name:
            lessons_of_type.append(lesson)
    return lessons_of_type


def filter_by_location(relevant_lessons):
    filtered_lessons = []
    for lesson in relevant_lessons:
        if lesson['location'] in locations:
            filtered_lessons.append(lesson)
    return filtered_lessons


def filter_by_date(lessons_of_type):
    relevant_lessons = []
    current_datetime = datetime.now()
    # Map the integer to the corresponding weekday name
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for lesson in lessons_of_type:
        date_str = lesson['from_date']
        comprehensive_from_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        date_str = lesson['oe_from_date']
        oe_from_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        # Get the weekday as an integer (Monday is 0, Sunday is 6)
        weekday_number = comprehensive_from_date.weekday()
        weekday_name = weekdays[weekday_number]
        if weekday_name in relevant_days and oe_from_date < current_datetime:
            relevant_lessons.append(lesson)
    return relevant_lessons


def filter_lessons(relevant_lessons):
    filtered_lessons = filter_by_date(relevant_lessons)
    if type_matter:
        filtered_lessons = filter_lessons_by_type(filtered_lessons)
    if location_matter:
        filtered_lessons = filter_by_location(filtered_lessons)
    return filtered_lessons


def get_relevant_lessons():
    sorted_entries = get_all_lessons()
    lessons_with_name = find_all_lessons_with_name(sorted_entries)

    relevant_lessons = filter_lessons(lessons_with_name)
    return relevant_lessons


def main():
    try:
        relevant_lessons = get_relevant_lessons()
        if len(relevant_lessons) != 0:
            print_lessons_enrolling_to(relevant_lessons)
            enroll_all = confirm_enrollment_in_all()
            if enroll_all:
                for lesson in relevant_lessons:
                    course_id = get_course_id(lesson)
                    enrol_in_lesson(course_id)
            else:
                for lesson in relevant_lessons:
                    print_lesson_information(lesson)
                    course_id = get_course_id(lesson)
                    enroll = confirm_enrollment_in_single_lesson(lesson)
                    if enroll:
                        enrol_in_lesson(course_id)
        else:
            print("no lessons found!")
    except Exception as e:
        print(e)
    print("end")


main()
