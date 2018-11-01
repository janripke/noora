#!/usr/bin/env python

import unittest
import os
import sys

BASE_DIR = os.path.abspath('.')
NOORA_DIR = BASE_DIR.split('test')[0] + "src"

sys.path.append(NOORA_DIR)

from src.org.noora.io.Properties import Properties
from src.org.noora.io.Property import Property
from src.org.noora.io.File import File
from src.org.noora.io.FileReader import FileReader
from src.org.noora.io.XmlFileReader import XmlFileReader
from src.org.noora.io.PropertyLoader import PropertyLoader


class TestXmlProperties(unittest.TestCase):
    def getFileReader(self, fileName):
        file = File(pathName=fileName)
        fileReader = FileReader(file)
        return fileReader      

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testProperties(self):
        properties = Properties()
        properties.setProperty("application.version", "1.0.0")
        self.assertEqual(properties.size(), 1, "invalid size")
        properties.clear()
        self.assertEqual(properties.size(), 0, "invalid size")

    def nnvl(self,parent):
      if parent!="":
        return parent+"."
      return parent
        
    def getElement(self, element, parent=""):
      len = element.__len__()
      result = []
      
      if len!=0:
        for index in range(len):
          child = element.__getitem__(index)

          tag = child.tag
          text = child.text
          if child.text!=None:
            text = text.strip()
          
          result.append([self.nnvl(parent)+tag,text])          
          
          
          items=self.getElement(child,self.nnvl(parent)+child.tag)
          for item in items:
            result.append(item)      
      return result
        
    def testXmlFileReader(self):
      file = File("project.xml")
      fileReader = XmlFileReader(file)
      stream = fileReader.read()


      properties = Properties()
      root = stream.getroot()
      for element in self.getElement(root):
        property=properties.getProperty(element[0])
        if property!=None:
          
          value = property.getValue()
          property.setValue(value+','+str(element[1]))
        else:
          properties.setProperty(element[0], str(element[1]))
        print(element)
      #for index in range(root.__len__()):
      #  print root.__getitem__(index)
        
          
      #for element in stream.iter():         
      #  if element.__len__()!=0:
      #    for index in range(element.__len__()):
      #      print element.__getitem__(index)
      
      print("------------------")
      #for element in stream.iter():  
        
              
      #  if element.text != None:
      #    if element.text.strip()!="":
      #      #print element.tag,"-->","'"+element.text+"'"            
      #      properties.setProperty(element.tag, element.text)
      #    else:
      #      pass
            #print element.tag
      fileReader.close()
      print("properties.size:",properties.size())
      for property in properties.list():
        print(property.getKey(),"-->",property.getValue())
 
        
    def testPropertyLoader(self):
        properties = Properties()        
        propertyLoader = PropertyLoader(properties)
        fileReader = self.getFileReader("test.conf")
        propertyLoader.load(fileReader)
        self.assertEqual(properties.size(), 4, "invalid size")
        property = properties.getProperty("ORACLE_USERS")
        self.assertEqual(len(eval(property.getValue())), 2, "invalid size")
        


if __name__ == '__main__':
    unittest.main()
