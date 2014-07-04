import os

from flask import Flask, request

from twilio import twiml

from old_section import SECTIONS

# Declare and configure application
app = Flask(__name__)

DEFAULT_TIMEOUT = 60

@app.route('/ivr/voice', methods=['POST'])
def voice():
    # Get the current conversation node
    language = request.args.get('language', 'robot')
    section_name = request.args.get('section', 'START')
    section = SECTIONS[section_name]

    prompt = section.get_prompt(language)
    response = twiml.Response()
    if section.gather_num_digits:
        with response.gather(numDigits=section.gather_num_digits, action="/ivr/gather?section=" + section_name,
                            timeout=DEFAULT_TIMEOUT) as gatherer:
            gatherer.say(prompt)
            # gather.play("path_to_greeting") # TODO (jmagnarelli): customize this per-caller if recognized
    else:
        response.say(prompt)
    return str(response)

@app.route('/ivr/gather', methods=['POST'])
def gather():
    language = request.args.get('language', 'robot')
    section_name = request.args.get('section', 'START')
    section = SECTIONS[section_name]

    response = twiml.Response()
    digits = request.form['Digits']
    dest = section.get_digit_destination(digits)
    resp = section.get_digit_response(digits, language)
    new_lang = section.changed_language(digits)
    if new_lang:
        language = new_lang
    response.say(resp)
    response.redirect("/ivr/voice?section=" + dest + "&language=" + language)
    return str(response)

# If PORT not specified by environment, assume development config.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
