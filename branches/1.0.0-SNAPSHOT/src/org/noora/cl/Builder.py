from org.noora.cl.Option import Option, OF_OPTION, OF_OPTIONARG

class Builder(object):

  def __init__(self):
    pass
  
#---------------------------------------------------------

  @staticmethod
  def getHelpDescriptions(options):
    """ Generate a list of help descriptions (one item per option)
      format:
        "-c", "--connector=<connector>" : description
    """
    descriptions = []
    
    for option in options:
      if option.getTypeFlag() & OF_OPTION:
        descriptions.append(Builder.getOptionHelpDescription(option))
      if option.getTypeFlag() & OF_OPTIONARG:
        descriptions.append(Builder.getOptionArgHelpDescription(option))
        
    return descriptions
      
#---------------------------------------------------------

  @staticmethod
  def getOptionHelpDescription(option):
    shortName = option.getShortName();
    longName = option.getLongName();
    
    opts = shortName if shortName else longName
    if shortName and longName:
      opts = "{0}, {1}".format(option.getShortName(), option.getLongName())
      
    return "{0:35} {1:40} ({2})".format(opts, option.getDescription(), "required" if option.isRequired() == 1 else "optional")
  
#---------------------------------------------------------

  @staticmethod
  def getOptionArgHelpDescription(option):  
    shortName = option.getShortName();
    longName = option.getLongName();
    
    opts = shortName if shortName else "{0}=<{1}>".format(longName, option.getValueDescription())
    if shortName and longName:
      opts = "{0}, {1}=<{2}>".format(option.getShortName(), option.getLongName(), option.getValueDescription())
          
    return "{0:35} {1:40} ({2})".format(opts, option.getDescription(), "required" if option.isRequired() == 1 else "optional")
  