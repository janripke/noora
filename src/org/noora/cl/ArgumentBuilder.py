class ArgumentBuilder(object):
  @staticmethod
  def build(*args):
    result = []
    for arg in args:
      option = arg
      
      if option:
        if option.hasValues():       
          result.append(option.getType()+"="+option.getValue())
    return result