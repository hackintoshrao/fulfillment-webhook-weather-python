# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    # Parsing the POST request body into a dictionary for easy access. 
    req_dict = json.loads(request.data)
    entity_type = ""
    entity_value = ""
    speech = ""
    # Accessing the fields on the POST request boduy of API.ai invocation of the webhook
    intent = req_dict["result"]["metadata"]["intentName"]

    entity_key_val = req_dict["result"]["parameters"]
    for key in entity_key_val:
	    entity_value = entity_key_val[key]
	    entity_type = key 
    
    # constructing the resposne string based on intent and the entity.
    if intent == "Platform exploration help":
	    if entity_type == "features":
		    if entity_value == "goals":
			    speech = """Here are the steps to update the goals: First, select the project (from the carousel) > click on an objective > update goals. i
			                Here you can drag the seeker to update the progress and then pick the date to assign the progress to that specific date. 
					Then hit save to record your progress."""
                    elif entity_value == "sign out":
			    speech = """Here are the steps to signout: Go to top right icon > profile > sign out and then click on it."""
                    else:
			    speech = """Currently I can only help you with udpating the goals and signing out. I could do more as I evolve."""

    else:
           speech = """Currently I can only help you with navigating to udpate the goals and signing out. I could do more as I evolve."""

    
    res = makeWebhookResult(speech)
    return res


def makeWebhookResult(speech):
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "source": "Build conversational interface for your app in 10 minutes."
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
