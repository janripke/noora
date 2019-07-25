from noora.rest.rest_request import RestRequest


class AzWebToken:
    @staticmethod
    def get():
        url = "http://169.254.169.254/metadata/identity/oauth2/token" \
              "?api-version=2018-02-01" \
              "&resource=https%3A%2F%2Fvault.azure.net"

        headers = {"Content-Type": "application/json", "Metadata": "true"}
        response = RestRequest.get(headers, url)
        print(response.status_code)
        content = response.json()
        print(content)
        return content


class AzWebKeyVaultSecret:
    @staticmethod
    def get(token, key_vault, value):
        url = "https://{}.vault.azure.net/secrets/{}/?api-version=2016-10-01".format(
            key_vault,
            value
        )
        bearer_token = "Bearer {}".format(token)
        headers = {"Content-Type": "application/json", "Authorization": bearer_token}
        response = RestRequest.get(headers, url)
        content = response.json()
        return content.get('value')