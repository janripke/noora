class ClassLoader:
    
    def __init__(self):
        pass
    
    def find(self, moduleName,className):
        mod = __import__(moduleName ,globals(), locals(), [''])
        clazz=getattr(mod,className)
        
        clazzInstance=clazz()
        return clazzInstance
    
    def findByPattern(self,pattern):
        patternList = pattern.split(".")
        listLength=len(patternList)
        className=patternList[listLength-1]
        moduleName=".".join(patternList[0:listLength-1])
        return self.find(moduleName, className)

    
   
        
