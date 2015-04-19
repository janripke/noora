#!/usr/bin/env python

class PropertyHelper:

  def __init__(self):
    pass
  
  @staticmethod
  def getUser(users, host, database):
    for user in users:
      if user[0].lower() == host.lower() and user[1].lower() == database.lower():
        return user[2]
    return None
  
  @staticmethod
  def getPasswd(users, host, database):
    for user in users:
      if user[0].lower() == host.lower() and user[1].lower() == database.lower():
        return user[3]
    return None

  

  @staticmethod
  def getMysqlUser(users, host, database):
    for user in users:
      if user[0].lower() == host.lower() and user[1].lower() == database.lower():
        return user[2]
    return None
  
  @staticmethod
  def getMysqlPasswd(users, host, database):
    for user in users:
      if user[0].lower() == host.lower() and user[1].lower() == database.lower():
        return user[3]
    return None

  @staticmethod
  def getPostgresqlUser(users, host, port, database):
    for user in users:
      if user[0].lower() == host.lower() and user[1].lower() == port.lower() and user[2].lower() == database.lower():
        return user[3]
    return None

  @staticmethod
  def getOracleUser(users, sid, scheme):
    for user in users:
      if user[0].lower() == sid.lower() and user[1].lower() == scheme.lower():
        return user[2]
    return None
  
  @staticmethod
  def getOraclePasswd(users, sid, scheme):
    for user in users:
      if user[0].lower() == sid.lower() and user[1].lower() == scheme.lower():
        return user[3]
    return None

