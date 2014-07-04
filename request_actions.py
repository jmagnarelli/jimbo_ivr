from twilio.rest import TwilioRestClient

from secrets import account_sid, auth_token, ivr_number, james_number

client = TwilioRestClient(account_sid, auth_token)

class RequestActions(object):

    @staticmethod
    def notify_punters(request, section):
        from_number = request.values.get('FROM', '')
        msg = "Someone from your IVR wants to go to Punter's. Oh, Joy! Their phone number is {0}, and" \
              "their section was {1}".format(from_number, section.name)
        message = client.messages.create(to=james_number, from_=ivr_number, body=msg)
        print message.sid

    @staticmethod
    def schedule_callback(request, section):
        from_number = request.values.get('FROM', '')
        msg = "Someone from your IVR wants to be called back. Oh, Joy! Their phone number is {0}, and their" \
              "section was {1}".format(from_number, section.name)
        message = client.messages.create(to=james_number, from_=ivr_number, body=msg)
        print message.sid