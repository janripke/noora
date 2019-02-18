class StreamHelper(object):
  def convert(self,stream):
    stream = stream.replace(chr(13)+chr(10),chr(10))
    stream = stream.replace(chr(13),chr(10)) 
    return stream

