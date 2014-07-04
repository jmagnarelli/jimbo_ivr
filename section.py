from request_actions import RequestActions

RAW_SECTIONS = {
    "START": {
        'num_digits_to_collect': 1,
        'prompt':{
            "english": "",
            "spanish": "",
            "robot": "Hello there. This is James Magnarelli. For English, press 1. Para espanol, marque numero dos."
                     "For a robot, press 3."
        },
        'digits':{
            "1":{
                "destination": "MAINMENU",
                "new_language": "english"
            },
            "2":{
                "destination": "MAINMENU",
                "new_language": "spanish"
            },
            "3":{
                "destination": "MAINMENU",
                "new_language": "robot"
            }
        }
    },
    "MAINMENU":{
        'num_digits_to_collect': 1,
        'prompt':{
            "english": "",
            "spanish": "Si, es espanol.",
            "robot": "This is the main menu. To return here at any time, press star. For Information about me, press 1. For Contact information and procedures, press 2. If you want to go to Punter's, press 3. For a mystery surprise, press 4. If you want to play a game, press 5. If you've changed your mind about Punter's, press 6. If this is an urgent matter, and you need to be put through to me directly, press 0. To repeat these options, press star."
        },
        "digits":{
            "1":{
                "destination": "INFO"
            },
            "2":{
                "destination": "CONTACT"
            },
            "3":{
                "destination": "PUNTERS"
            },
            "4":{
                "destination": "MYSTERY"
            },
            "5":{
                "destination": "GAME"
            },
            "6":{
                "destination": "PUNTERS"
            },
            "0":{
                "destination": "PUTTHROUGH"
            },


        }
    },
    "INFO":{
        'num_digits_to_collect': 1,
        'prompt':{
            "english": "",
            "spanish": "",
            "robot": "This is my personal information. To return to the start menu, press star."
        }
    },
    "CONTACT":{
        'num_digits_to_collect': 1,
        'prompt':{
            "english": "",
            "spanish": "",
            "robot": "For my website, head to w w w dot magnarelli dot org . That's m a g n a r e l l i dot org. You"
                     "can email me at j m a g n a r e at gmail dot com. If you'd like me to call you later at this"
                     "number, press 1. If this is an urgent matter, and you need to be put through to me directly,"
                     "press 0. To return to the start menu, press star."
        },
        'digits':{
            "1":{
                "action": RequestActions.schedule_callback,
                "destination": "BYE",
                "responses": {
                    "english": "",
                    "spanish": "",
                    "robot": "Great. I will call you back later at this number."
                }
            },
            "0":{
                "destination": "PUTTHROUGH"
            }
        }
    },
    "PUNTERS":{
        'num_digits_to_collect': 1,
        'prompt':{
            "english": "",
            "spanish": "",
            "robot": "You like Punter's, too? Awesome. Let's go together. If you'd like to meet there now, press 1. If you'd like to meet there later, press 2 to leave your number for a callback. To return to the start menu, press star"
        },
        'digits':{
            "1":{
                "action": RequestActions.notify_punters,
                "destination": "BYE",
                "responses": {
                    "english": "",
                    "spanish": "",
                    "robot": "Sweet. Let's go."
                }
            },
            "2":{
                "action": RequestActions.schedule_callback,
                "destination": "BYE",
                "responses": {
                    "english": "",
                    "spanish": "",
                    "robot": "Great, you left a number!"
                }
            }
        }
    },
    "MYSTERY":{
        'num_digits_to_collect': 1,
        'prompt':{
            "english": "/sounds/heman_short.mp3",
            "spanish": "/sounds/heman_short.mp3",
            "robot": "/sounds/heman_short.mp3; To repeat this message, press 1. To return to the main menu, press star."
        },
        'digits':{
            "1":{
                "destination": "MYSTERY"
            }
        }

    },
    "GAME":{
        'num_digits_to_collect': 1,
        'prompt':{
            "english": "",
            "spanish": "",
            "robot": "You are standing at the end of a road..."
        }
    },
    "PUTTHROUGH":{
        'num_digits_to_collect': 0,
        'prompt':{
            "english": "",
            "spanish": "",
            "robot": "You are being put through to me. Please standby."
        }
    },
    "BYE":{
        'num_digits_to_collect': 0,
        'prompt':{
            "english": "",
            "spanish": "",
            "robot": "Goodbye"
        }
    }
}


class SectionResponse(object):
    def __init__(self, text, is_link):
        self.text = text
        self.is_link = is_link

    @property
    def should_say(self):
        return not self.is_link

class Section(object):
    def __init__(self, name, prompt, gather_num_digits, digits_dict={}):
        self.name = name
        self.prompt = prompt
        self.gather_num_digits = gather_num_digits
        self.digits_dict = dict(digits_dict.items() + {"*": {'destination': "MAINMENU"}}.items())

    def changed_language(self, digits):
        return self.digits_dict.get(digits, {}).get('new_language', False)

    def get_digit_destination(self, digits):
        return self.digits_dict.get(digits, {}).get('destination', 'BYE')

    def get_digit_response(self, digits, language):
        if digits not in self.digits_dict:
            return "Invalid input. Sorry about that."
        resp = self.digits_dict[digits].get('responses', {}).get(language, '')
        resps = resp.split(';')
        retVal = []
        for r in resps:
            if r.startswith('/'):
                retVal.append(SectionResponse(r, True))
            else:
                retVal.append(SectionResponse(r, False))
        return retVal


    def get_prompt(self, language):
        prompt = self.prompt.get(language, '')
        prompts = prompt.split(';')
        retVal = []
        for p in prompts:
            if p.startswith('/'):
                retVal.append(SectionResponse(p, True))
            else:
                retVal.append(SectionResponse(p, False))
        return retVal

    def get_digit_action(self, digits):
        return self.digits_dict.get(digits, {}).get('action', lambda r, s: None)

SECTIONS = {}
for name, sect in RAW_SECTIONS.iteritems():
    SECTIONS[name] = Section(name,
                             sect['prompt'],
                             sect['num_digits_to_collect'],
                             sect.get('digits', {}))