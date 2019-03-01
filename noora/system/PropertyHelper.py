import os
import json
from copy import copy


# FIXME: write a proper docstring
def get_database_folder(database, folder_aliases):
    if folder_aliases:
        for folder_alias in folder_aliases:
            alias = folder_alias[0]
            if database == alias:
                return folder_alias[1]
    return database


def get_mssql_properties(users, host, schema):
    """
    For a list of user tuples, find the first occurrence that matches host and database.

    :param users: list containing a sequence of AT LEAST (host, schema, username, password)
    :param host: the hostname to match
    :param schema: the schema to match
    :return: a dict containing host, schema, username, password, port
    """
    for user in users:
        if user[0].lower() == host.lower() and user[1].lower() == schema.lower():
            res = {
                'host': host,
                'schema': schema,
                # Backwards compatibility with old project files
                'port': user[4] if len(user) > 4 else None,
                'username': user[2],
                'password': user[3],
            }
            return res

    return None


def get_mysql_properties(users, host, database):
    """
    For a list of user tuples, find the first occurrence that matches host and database.

    :param users: list containing a sequence of AT LEAST (host, database, username, password)
    :param host: the hostname to match
    :param database: the database to match
    :return: a dict containing host, database, username, password, port
    """
    for user in users:
        if user[0].lower() == host.lower() and user[1].lower() == database.lower():
            res = {
                'host': host,
                'database': database,
                # Backwards compatibility with old project files
                'port': user[4] if len(user) > 4 else None,
                'username': user[2],
                'password': user[3],
            }
            return res

    return None


def get_postgres_user(users, host, port, database):
    """
    For a list of host/port/database/user combinations, return the username that matches the
    host, port, database and user.

    :param users: list containing a sequence of AT LEAST (host, port, database, username)
    :param host: The hostname to match
    :param port: The port to match
    :param database: The database to match
    :return: A username or None
    """
    for user in users:
        if user[0].lower() == host.lower() and user[1].lower() == port.lower() and \
                user[2].lower() == database.lower():
            return user[3]
    return None


def get_oracle_user(users, sid, scheme):
    """
    For a list of sid/scheme/user combinations, return the username that matches the
    sid, scheme and user.

    :param users: list containing a sequence of AT LEAST (sid, scheme, username)
    :param sid: The Site Identifier (SID) to match
    :param scheme: The scheme to match
    :return: A username or None
    """
    for user in users:
        if user[0].lower() == sid.lower() and user[1].lower() == scheme.lower():
            return user[2]
    return None


def get_oracle_passwd(users, sid, scheme):
    """
    For a list of sid/scheme/user/password combinations, return the password that matches the
    sid, scheme and user.

    :param users: list containing a sequence of AT LEAST (sid, scheme, username, password)
    :param sid: The Site Identifier (SID) to match
    :param scheme: The scheme to match
    :return: A password or None
    """
    for user in users:
        if user[0].lower() == sid.lower() and user[1].lower() == scheme.lower():
            return user[3]
    return None


def get_profile(properties):
    """
    Retrieve the profile for the database project in the properties.
    """
    profile = None
    project = properties.get('project')
    if project:
        # load the users from the credentials file, if present
        home_dir = properties.get('home.dir')
        credentials_file = os.path.join(home_dir, '.noora', 'credentials.json')
        if os.path.isfile(credentials_file):
            f = open(credentials_file, 'r')
            credentials = json.load(f)
            f.close()

            profile = credentials.get(project)
    return profile
