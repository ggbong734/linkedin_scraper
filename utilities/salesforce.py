import json

from simple_salesforce import Salesforce, format_soql

class SalesforceAdapter:
    def __init__(self):
        self.format_soql = format_soql
        with open('credentials.json') as json_file:
            credentials = json.load(json_file)
            self.environment = credentials['environment']
            print(f"Running on {self.environment} environment")
            if self.environment == 'prod':
                result = credentials['data']['prod']
                self._sf = Salesforce(
                    username=result['username'],
                    password=get_decoded_string(result['access']),
                    security_token=result['security_token'])
            elif self.environment == 'scratch':
                result = credentials['data']['scratch']
                self._sf = Salesforce(
                    session_id=result['access_token'],
                    instance_url=result['instance_url'])
            else:
                raise Exception('environment label in credentials.json is incorrect')

    def get_instance(self):
        return self._sf