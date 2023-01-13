# host=postgresqlserver-runapi-dev.postgres.database.azure.com port=5432 dbname=runapi user=runapi_owner@postgresqlserver-runapi-dev password={your_password} sslmode=require"

def connection_credentials(connection_string: str) -> dict:
    """
    Returns a dict containing the connection credentials
    The following format is expected for the connection_string.
    In the example below a postgresql connection string is used.
    host=localhost, port=5432, dbname=acme, username=acme_owner, password=acme_owner, sslmode=require

    :type connection_string: str
    :param connection_string: A connection string;
    """

    key_strings = connection_string.split(",")
    result = {}
    for key_string in key_strings:
        key_value_pair = key_string.split("=")
        key = key_value_pair[0].replace(" ", "")
        value = key_value_pair[1]
        result[key] = value
    return result



connection_string = "host=localhost, port=5432, dbname=runapi, username=runapi_owner, password=runapi_owner, sslmode=require"
print(connection_credentials(connection_string))

# key_strings = connection_string.split(",")
# result = {}
# for key_string in key_strings:
#     print(key_string, key_string.split("="))
#     key_value_pair = key_string.split("=")
#     key = key_value_pair[0].replace(" ", "")
#     value = key_value_pair[1]
#     result[key] = value
#
# print(result)
