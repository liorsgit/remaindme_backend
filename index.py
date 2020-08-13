from flask import Flask, request
import boto3
from firebase_admin import messaging
import firebase_admin
from firebase_admin import credentials


# This main.py file represents the cloud based backend of 'remaind me' program
# used tech: AWS, DynamoDB, Firebase, Flask

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('token')

app = Flask(__name__)

@app.route("/", methods=['GET'])
def main():
        token = request.args.get("token")
        table.put_item(
   Item={
        'token': token
    }
)
        return True

@app.route("/broadcast", methods=['GET'])
def notify():

        tokens = []

        # get all parameters
        try:
                head = request.args.get("head")
                body = request.args.get("body")
                long = request.args.get("long")
                lati = request.args.get("lati")

        except Exception as e:
                print('Failed receiveing parameters from DB, {}'.format(e))
                return e
    
        # get all tokens from db
        try:
                response = table.scan()
                for i in response['Items']:
                        tokens.append(token['token'])
                print(tokens)

        except Exception as e:
                print('Failed receiveing tokens from DB, {}'.format(e))
                return e

        # initialize app
        try:
                cred = credentials.Certificate('/home/ubuntu/key.json')
                app = firebase_admin.initialize_app(cred)

        except Exception as e:
                print('Failed initializing firebase app, {}'.format(e))
                return e

        # define message
        for tokenid in tokens:
                message = None
                message = messaging.Message(
                    data={
                        'head': head,
                        'body': body,
                        'longitude': long,
                        'latitude': lati,
                    },
                    token=tokenid)

                # send message
                try:
                        response = messaging.send(message)
                except Exception as e:
                        print('Failed sending message, {}'.format(e))
                        return r
                    
        return True


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
