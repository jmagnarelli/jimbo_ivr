import os

from flask import Flask, request

from twilio import twiml

# Declare and configure application
app = Flask(__name__)

DEFAULT_TIMEOUT = 60

class Section(object):
    def __init__(self, name, prompt, gather, num_digits, digits_dict):
        self.name = name
        self.prompt = prompt
        self.gather = gather
        self.num_digits = num_digits
        self.valid_digits_to_resp_and_dest = digits_dict

    def get_resp_and_dest(self, digits):
        return self.valid_digits_to_resp_and_dest.get(digits, ("Invalid input. Sorry about that", self.name))

# Initialize conversation flow
# TODO (jmagnarelli): move this to json or something
SECTS = [
    Section("START",
            "Hello there. This is James Magnarelli. For English, press 1. Para espanol, marque numero dos",
            True,
            1,
            {"1": ("Hey, that's english!", "MAINMENU"),
            "2": ("Ay de mi! Es espanol!", "MAINMENU"),
            "*": ("", "START")}),
    Section("MAINMENU",
            "For Information about me, press 1. For Contact information and procedures, press 2. If you want to go to Punter's, press 3. For a mystery surprise, press 4. If you want to play a game, press 5. If you've changed your mind about Punter's, press 6. If this is an urgent matter, and you need to be put through to me directly, press 0. To repeat these options, press star.",
            True,
            1,
            {"1": ("", "INFO"),
            "2": ("", "CONTACT"),
            "3": ("", "PUNTERS"),
            "4": ("", "MYSTERY"),
            "5": ("", "GAME"),
            "6": ("", "PUNTERS"),
            "0": ("", "PUTTHROUGH"),
            "*": ("", "MAINMENU")}),
    Section("INFO",
            "This is my personal information. To return to the start menu, press star.",
            True,
            1,
            {"*": ("", "START")}),
    Section("CONTACT",
            "Blah, blah, blah. This is my contact information. To leave a number for me to call back later, press 1. To return to the start menu, press star.",
            True,
            1,
            {"1": ("Great, you left a number!", "BYE"),
            "*": ("", "START")}),
    Section("PUNTERS",
            "You like Punter's, too? Awesome. Let's go together. If you'd like to meet there now, press 1. If you'd like to meet there later, press 2 to leave your number for a callback. To return to the start menu, press star",
            True,
            1,
            {"1": ("Sweet. Let's go.", "BYE"),
            "2": ("Great, you left a number!", "BYE"),
            "*": ("", "START")}),
    Section("MYSTERY",
            "This is a MYSTERY!!!",
            True,
            1,
            {"*": ("", "START")}),
    Section("GAME",
            "You are standing at the end of a road...",
            True,
            1,
            {"*": ("", "START")}),
    Section("PUTTHROUGH",
            "You are being put through to me. Please standby.",
            True,
            1,
            {"*": ("", "START")}),
    Section("BYE",
            "Goodbye",
            False,
            0,
            {})
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
        with response.gather(numDigits=section.num_digits, action="/ivr/gather?section=" + section_name,
                               timeout=DEFAULT_TIMEOUT) as gatherer:
            gatherer.say(section.prompt)
            # gather.play("path_to_greeting") # TODO (jmagnarelli): customize this per-caller if recognized
    else:
        response.say(section.prompt)
    return str(response)

@app.route('/ivr/gather', methods=['POST'])
def gather():
    section_name = request.args.get('section', 'START')
    section = SECTIONS[section_name]

    response = twiml.Response()
    digits = request.form['Digits']
    resp, dest = section.get_resp_and_dest(digits)
    response.say(resp)
    response.redirect("/ivr/voice?section=" + dest)
    return str(response)

# If PORT not specified by environment, assume development config.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
