from org.noora.app.AppException import AppException


class Appable(object):
  def checkRequiredOptions(self):
    raise AppException("method not implemented")
