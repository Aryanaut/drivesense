from twilio.rest import Client

class sms:
    def __init__(self):
        account_sid = 'ACa236584f1a676b09632c019e881575db'
        auth_token = '2c7c6c1214ecfc2c07adf74b451dec28'
        client = Client(account_sid, auth_token)
    
    def sendMSG(number, body)
        message = client.messages \
            .create(
         body=body,
         from_='+13343262498',
         to=number
     )