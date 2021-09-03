from unittest import TestCase
from unittest.mock import patch, mock_open

from utilities.salesforce import SalesforceAdapter

class SalesforceAdapterTest(TestCase):
    def test__init__(self):
        credentials = {
            'environment': 'prod',
            'data': {
                'prod': {
                    'username': 'username_1',
                    'access': 'access_1',
                    'security_token': 'security_token_1'
                },
                'scratch': {
                    'access_token': 'access_token_1',
                    'instance_url': 'instance_url_1'
                }
            }
        }
        with patch('builtins.open', mock_open(read_data="test")) as mock_file,\
                patch('utilities.salesforce.json') as mock_json,\
                patch('utilities.salesforce.Salesforce') as mock_salesforce_class,\
                patch('utilities.salesforce.get_decoded_string') as mock_get_decoded_string,\
                patch('utilities.salesforce.print'):
            mock_json.load.return_value = credentials
            mock_get_decoded_string.return_value = 'password_1'
            sf = SalesforceAdapter().get_instance()
            mock_salesforce_class.assert_called_with(
                username='username_1', password='password_1', security_token='security_token_1')
            mock_get_decoded_string.assert_called_with('access_1')
            credentials['environment'] = 'scratch'
            sf = SalesforceAdapter().get_instance()
            mock_salesforce_class.assert_called_with(
                session_id='access_token_1', instance_url='instance_url_1')
            credentials['environment'] = 'aaaa'
            try: sf = SalesforceAdapter().get_instance()
            except Exception as e: self.assertEqual(str(e), 'environment label in credentials.json is incorrect')
            mock_file.assert_called_with('credentials.json')