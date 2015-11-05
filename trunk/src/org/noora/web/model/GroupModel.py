from org.noora.web.model.Model import Model


class GroupModel(Model):
  def __init__(self, db=None):
    Model.__init__(self, db)


  def getGroup(self, id):
    db = self.getDatabase()
    try:
      return db.select('groups', where='id=$id', vars=locals())[0]
    except IndexError:
      return None

  def getGroupByName(self, name):
    db = self.getDatabase()
    try:
      return db.select('groups', where='usergroup=$name', vars=locals())[0]
    except IndexError:
      return None

