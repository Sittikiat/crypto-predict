from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)

api=Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('data.csv')
        data = data.to_dict('records')
        return {'BTC-USD' : data}, 200


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Date', required=True)
        parser.add_argument('Close', required=True)
        args = parser.parse_args()

        data = pd.read_csv('data.csv')

        new_data = pd.DataFrame({
            'Date'      : [args['Date']],
            'Close'     : [args['Close']],
        })

        data = data.append(new_data, ignore_index = True)
        data.to_csv('data.csv', index=False)
     
        return {'data' : new_data.to_dict('records')}, 201
   
        

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Date', required=True)
        args = parser.parse_args()

        data = pd.read_csv('data.csv')

        data = data[data['Date'] != args['Date']]

        data.to_csv('data.csv', index=False)
        return {'message' : 'Record deleted successfully.'}, 200


# Add URL endpoints
api.add_resource(Users, '/data')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)