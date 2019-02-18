from org.noora.cl.Option import Option


class OptionFactory(object):
  @staticmethod
  def newOption(type=None, longType=None, hasArguments=False, required=False, description=None):
    return Option(type, longType, hasArguments, required, description)
