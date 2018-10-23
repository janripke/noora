import os
import json


class PropertyHelper:
    def __init__(self):
        pass

    @staticmethod
    def get_database_folder(database, folder_aliases):
        if folder_aliases:
            for folder_alias in folder_aliases:
                alias = folder_alias[0]
                if database == alias:
                    return folder_alias[1]
        return database

    @staticmethod
    def get_mssql_user(users, host, schema):
        for user in users:
            if user[0].lower() == host.lower() and user[1].lower() == schema.lower():
                return user[2]
        return None

    @staticmethod
    def get_mssql_password(users, host, schema):
        for user in users:
            if user[0].lower() == host.lower() and user[1].lower() == schema.lower():
                return user[3]
        return None

    @staticmethod
    def get_mysql_user(users, host, database):
        for user in users:
            if user[0].lower() == host.lower() and user[1].lower() == database.lower():
                return user[2]
        return None

    @staticmethod
    def get_mysql_passwd(users, host, database):
        for user in users:
            if user[0].lower() == host.lower() and user[1].lower() == database.lower():
                return user[3]
        return None

    @staticmethod
    def get_postgres_user(users, host, port, database):
        for user in users:
            if user[0].lower() == host.lower() and user[1].lower() == port.lower() and user[2].lower() == database.lower():
                return user[3]
        return None

    @staticmethod
    def get_oracle_user(users, sid, scheme):
        for user in users:
            if user[0].lower() == sid.lower() and user[1].lower() == scheme.lower():
                return user[2]
        return None

    @staticmethod
    def get_oracle_passwd(users, sid, scheme):
        for user in users:
            if user[0].lower() == sid.lower() and user[1].lower() == scheme.lower():
                return user[3]
        return None

    @staticmethod
    def get_profile(properties):
        # retrieve the profile of database project
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
