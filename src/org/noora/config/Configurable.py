#!/usr/bin/env python
from org.noora.io.IOException import IOException

class Configurable:

  def __init__(self):
    pass

  def load(self):
    raise IOException("method not implemented")

  def getProperty(self, name):
    raise IOException("method not implemented")

  def setProperty(self, name, value):
    raise IOException("method not implemented")

