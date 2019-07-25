import os
from noora.az.az_web import AzWebKeyVaultSecret, AzWebToken


class CredentialHelper:

    @staticmethod
    def get_credentials(res):
        platform = os.environ.get('PLATFORM', 'local')
        key_vault = os.environ.get('KEY_VAULT', None)

        if platform == 'azure':
            token = AzWebToken.get()
            access_token = token.get('access_token')

            username_key = res['username']
            password_key = res['password']
            res['username'] = AzWebKeyVaultSecret.get(access_token, key_vault, username_key)
            res['password'] = AzWebKeyVaultSecret.get(access_token, key_vault, password_key)

        return res