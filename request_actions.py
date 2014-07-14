from twilio.rest import TwilioRestClient

from secrets import account_sid, auth_token, ivr_number, james_number

client = TwilioRestClient(account_sid, auth_token)

class RequestActions(object):

    @staticmethod
    def notify_punters(request, section):
        from_number = request.values.get('From', '')
        msg = "Immediate Punter's request received. Phone number={0}, section={1}".format(from_number, section.name)
        message = client.messages.create(to=james_number, from_=ivr_number, body=msg)
        print message.sid

    @staticmethod
    def schedule_callback(request, section):
        from_number = request.values.get('From', '')
        msg = "Callback request received. Phone number={0}, section={1}".format(from_number, section.name)
        message = client.messages.create(to=james_number, from_=ivr_number, body=msg)
        print message.sid