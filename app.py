import os

from flask import Flask, request

from twilio import twiml

# Declare and configure application
app = Flask(__name__)

DEFAULT_TIMEOUT = 60

class Section(object):
    def __init__(self, name, prompt, gather, digits_dict):
        self.name = name
        self.prompt = prompt
        self.gather = gather
        self.valid_digits_to_resp_and_dest = digits_dict

    def get_resp_and_dest(self, digits):
        return self.valid_digits_to_resp_and_dest.get(digits, ("Invalid input. Sorry about that", self.name))

# Initialize conversation flow
# TODO (jmagnarelli): move this to json or something
SECTS = [
    Section("START",
            "Hello there. This is James Magnarelli. For English, press 1. Para espanol, marque numero dos",
            True,
            {"1": ("Hey, that's english!", "START"),
            "2": ("Ay de mi! Es espanol!", "START")}
        )
]
SECTIONS = {}
for sect in SECTS:
    SECTIONS[sect.name] = sect

@app.route('/ivr/voice', methods=['POST'])
def voice():
    # Get the current conversation node
    section_name = request.args.get('section', 'START')
    section = SECTIONS[section_name]

    response = twiml.Response()
    if section.gather:
        with response.gatherer(numDigits=section.num_digits, action="/ivr/gather?section=" + section_name,
                               timeout=DEFAULT_TIMEOUT) as gatherer:
            gatherer.say(section.prompt)
            # gather.play("path_to_greeting") # TODO (jmagnarelli): customize this per-caller if recognized
    else:
        response.say(section.prompt)
    return str(response)

@app.route('/ivr/gather', methods=['POST'])
def gather():
    section = request.args.get('section', 'START')
    response = twiml.Response()
    digits = request.form['Digits']
    resp, dest = section.get_resp_and_dest(digits)
    response.say(resp)
    resp.redirect("/ivr/voice?section=" + dest)
    return str(response)

# If PORT not specified by environment, assume development config.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
