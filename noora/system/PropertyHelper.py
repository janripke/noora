import os
import json


# FIXME: write a proper docstring
def get_database_folder(database, folder_aliases):
    if folder_aliases:
        for folder_alias in folder_aliases:
            alias = folder_alias[0]
            if database == alias:
                return folder_alias[1]
    return database


def get_mssql_user(users, host, schema):
    """
    For a list of host/schema/user combinations, return the username that matches the host
    and schema.

    :param users: list containing a sequence of AT LEAST (host, schema, username)
    :param host: The hostname to match
    :param schema: The schema name to match
    :return: A matched username or None
    """
    for user in users:
        if user[0].lower() == host.lower() and user[1].lower() == schema.lower():
            return user[2]
    return None


def get_mssql_password(users, host, schema):
    """
    For a list of host/schema/user/password combinations, return the password that matches the
    host, schema and user.

    :param users: list containing a sequence of AT LEAST (host, schema, username, password)
    :param host: The hostname to match
    :param schema: The schema name to match
    :return: A password or None
    """
    for user in users:
        if user[0].lower() == host.lower() and user[1].lower() == schema.lower():
            return user[3]
    return None


def get_mysql_user(users, host, database):
    """
    For a list of host/database/user combinations, return the username that matches the
    host, database and user.

    :param users: list containing a sequence of AT LEAST (host, database, username)
    :param host: The hostname to match
    :param database: The database to match
    :return: A username or None
    """
    for user in users:
        if user[0].lower() == host.lower() and user[1].lower() == database.lower():
            return user[2]
    return None


def get_mysql_passwd(users, host, database):
    """
    For a list of host/database/user/password combinations, return the password that matches the
    host, database and user.

    :param users: list containing a sequence of AT LEAST (host, database, username, password)
    :param host: The hostname to match
    :param database: The database to match
    :return: A password or None
    """
    for user in users:
        if user[0].lower() == host.lower() and user[1].lower() == database.lower():
            return user[3]
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
