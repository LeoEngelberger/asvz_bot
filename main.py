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

# get id from detail view on schalter.asvz.ch exp: https://schalter.asvz.ch/tn/lessons/534848
course_id = "534848"

# get auth token by looking for member_info package under network in the inspector of your browser of choice
# it's the really long encrypted string
authorization_token = \
 "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
conn = http.client.HTTPSConnection("schalter.asvz.ch")
payload = ''
headers = {
  'Authorization': f'Bearer {authorization_token}'
}

url = "/tn-api/api/Lessons/%s/Enrollment" % course_id

print(url)

conn.request("POST", url, payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))