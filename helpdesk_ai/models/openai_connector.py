from odoo import models, api, fields, _
import keyring

service_name = 'OPEN_AI'
username = 'zeyadwagdy'


def get_secret_key():
    api_key = False
    try:
        api_key = keyring.get_password(service_name, username)
        if not api_key:
            raise Exception('API Key not found')
    except Exception as e:
        raise Exception('API Key not found')
    return api_key



class OpenAIConnector(models.Model):
    _name = 'openai.connector'
    _description = 'OpenAI Connector'

    # Methods
    @api.model
    def get_api_key(self):
        return get_secret_key()
