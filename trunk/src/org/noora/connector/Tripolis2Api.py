import logging
import sys
from suds.client import Client
from suds.multipart import MultipartFilter
from suds.plugin import MessagePlugin
from suds.sax.element import Element
from suds import WebFault

#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
#logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
from suds.sax.text import Text


class Tripoli2ApiException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        print "\r\n" + self.message

class AuthInfo:
    def __init__(self, client, username, password):
        tns = ('tns', 'http://services.tripolis.com/')
        self.__auth_info = Element('authInfo', ns=tns)
        client = Element('client').setText(client)
        username = Element('username').setText(username)
        password = Element('password').setText(password)
        self.__auth_info.append(client)
        self.__auth_info.append(username)
        self.__auth_info.append(password)

    def get(self):
        return self.__auth_info

class WorkspaceService:
    def __init__(self, auth_info):
        self.__url = 'https://td41.tripolis.com/api2/soap/WorkspaceService?wsdl'
        self.__client = Client(self.__url, plugins = [MultipartFilter()])

        ns0 = "http://common.services.tripolis.com/"
        ns1 = "http://request.services.tripolis.com/"
        ns2 = "http://response.services.tripolis.com/"
        ns3 = "http://services.tripolis.com/"
        ns4 = "http://workspace.services.tripolis.com/"

        self.__client.add_prefix('ns0', ns0)
        self.__client.add_prefix('ns1', ns1)
        self.__client.add_prefix('ns2', ns2)
        self.__client.add_prefix('ns3', ns3)
        self.__client.add_prefix('ns4', ns4)

        self.__client.set_options(soapheaders=auth_info.get())

    def getAll(self):
        service_request = self.__client.factory.create('ns1:ServiceRequest')
        return self.__client.service.getAll(service_request)

    """
    Returns a Workspace object or None if not found. An example of a Workspace object:
    (Workspace){
      id = "qvo8NMAolbA_3AFrodmdgQ"
      label = "kpncompleetdev"
      name = "kpncompleetdev"
      contactDatabaseId = "3nnH+KDcs9N8TlT6WqeEeg"
      publicDomainName = None
      bounceDomainName = None
      listUnsubscribeHeader = False
    }
    Field is one of the attributes of a Workspace object, i.e. 'name'
    """
    def getByField(self, field, value):
        for workspace in self.getAll().workspaces.workspace:
            if workspace[field] == value:
                return workspace

#print WorkspaceService().getByField('name', 'kpncompleetdev')


class DirectEmailTypeService:
    def __init__(self, auth_info):
        self.__url = 'https://td41.tripolis.com/api2/soap/DirectEmailTypeService?wsdl'
        self.__client = Client(self.__url, plugins = [MultipartFilter()])

        ns0 = "http://common.services.tripolis.com/"
        ns1 = "http://request.services.tripolis.com/"
        ns2 = "http://response.services.tripolis.com/"
        ns3 = "http://services.tripolis.com/"
        ns4 = "http://type.directemail.services.tripolis.com/"

        self.__client.add_prefix('ns0', ns0)
        self.__client.add_prefix('ns1', ns1)
        self.__client.add_prefix('ns2', ns2)
        self.__client.add_prefix('ns3', ns3)
        self.__client.add_prefix('ns4', ns4)

        self.__client.set_options(soapheaders=auth_info.get())

    """
    Returns a list of DirectEmailType objects or None if not workspace found, i.e.
    [(DirectEmailType){
       id = "OmJE+2eqsaLTSwPcIsPl2w"
       label = "Fase1 mails"
       name = "mails"
       fromName = "KPN"
       fromAddress = "publicaties@emailservice-kpn.com"
       toEmailFieldId = "j2j6ec3aAQn+zNNj5j8OpA"
       replyToAddress = None
       externalHtmlUrl = None
       externalTextUrl = None
       enableWysiwygEditor = False
       encoding = "UTF8"
       enableAttachments = False
    },
    ...]
    """
    def getByWorkspaceId(self, workspace_id):
        request = self.__client.factory.create('ns1:WorkspaceIDRequest')
        request.workspaceId = workspace_id

        try:
            response = self.__client.service.getByWorkspaceId(request)
            return response.directEmailTypes.directEmailType
        except WebFault as e:
            if e.fault.detail.errorResponse.errors.error.message == 'workspaceId not found':
                return None
            raise Tripoli2ApiException(e.fault.detail.errorResponse.errors.error.message)

#print DirectEmailTypeService().getByWorkspaceId('qvo8NMAolbA_3AFrodmdgQ')

class DirectEmailService:
    def __init__(self, auth_info):
        self.__url = 'https://td41.tripolis.com/api2/soap/DirectEmailService?wsdl'
        self.__client = Client(self.__url, plugins = [MultipartFilter()])

        ns0 = "http://common.services.tripolis.com/"
        ns1 = "http://directemail.services.tripolis.com/"
        ns2 = "http://request.services.tripolis.com/"
        ns3 = "http://response.services.tripolis.com/"
        ns4 = "http://services.tripolis.com/"

        self.__client.add_prefix('ns0', ns0)
        self.__client.add_prefix('ns1', ns1)
        self.__client.add_prefix('ns2', ns2)
        self.__client.add_prefix('ns3', ns3)
        self.__client.add_prefix('ns4', ns4)

        self.__client.set_options(soapheaders=auth_info.get())

    """
    Returns a list of DirectEmailForListing objects or None if not workspace found, i.e.
    [(DirectEmailForListing){
     id = "Yy2tB_Q2nS9bPIwy7RzKEg"
     directEmailTypeId = "fcw6GMjj1fk__uaAFGsVFQ"
     label = "09_reset_password"
     name = "09_reset_password"
     subject = "Wachtwoord reset FLITS helpdesk applicatie"
     fromName = "KPN"
     fromAddress = "publicaties@emailservice-kpn.com"
     replyToAddress = None
     description = None
     author = "erwin.rohde@2organize.com"
     modifiedAt = 2016-02-01 13:29:59+01:00
     isArchived = False
    },
    ...]
    """
    def getByDirectEmailTypeId(self, direct_email_type_id):
        request = self.__client.factory.create('ns2:DirectEmailTypeIDRequest')
        request.directEmailTypeId= direct_email_type_id
        request.paging.pageNr = 1
        request.paging.pageSize = 1000
        request.sorting.sortBy = 'name'
        request.sorting.sortOrder = 'ASC'

        try:
            response = self.__client.service.getByDirectEmailTypeId(request)
            # response.directEmails is an empty string, of no emails are in the direct email type
            if isinstance(response.directEmails, Text):
                return []
            return response.directEmails.directEmail
        except WebFault as e:
            if e.fault.detail.errorResponse.errors.error.message == 'directEmailTypeId not found':
                return None
            raise Tripoli2ApiException(e.fault.detail.errorResponse.errors.error.message)

    def update(self, direct_email_for_listing, tripolis_direct_email):

        request = self.__client.factory.create('UpdateDirectEmailRequest')
        request.id = direct_email_for_listing.id
        request.label = tripolis_direct_email.getLabel()
        request.name = tripolis_direct_email.getName()
        request.subject = unicode(tripolis_direct_email.getSubject(), encoding='utf-8')
        request.htmlSource = unicode(tripolis_direct_email.getHtml(), encoding='utf-8')
        request.textSource = unicode(tripolis_direct_email.getText(), encoding='utf-8')
        request.fromName = unicode(tripolis_direct_email.getFromName(), encoding='utf-8')
        request.fromAddress = tripolis_direct_email.getFromAddress()
        request.replyToAddress = tripolis_direct_email.getReplyTo()

        try:
            return self.__client.service.update(request).id
        except WebFault as e:
            raise Tripoli2ApiException(e.fault.detail.errorResponse.errors.error.message)

    def create(self, direct_email_type_id, tripolis_direct_email):

        request = self.__client.factory.create('CreateDirectEmailRequest')
        request.directEmailTypeId = direct_email_type_id
        request.label = tripolis_direct_email.getLabel()
        request.name = tripolis_direct_email.getName()
        request.subject = unicode(tripolis_direct_email.getSubject(), encoding='utf-8')
        request.htmlSource = unicode(tripolis_direct_email.getHtml(), encoding='utf-8')
        request.textSource = unicode(tripolis_direct_email.getText(), encoding='utf-8')
        request.fromName = unicode(tripolis_direct_email.getFromName(), encoding='utf-8')
        request.fromAddress = tripolis_direct_email.getFromAddress()
        request.replyToAddress = tripolis_direct_email.getReplyTo()

        try:
            return self.__client.service.create(request).id
        except WebFault as e:
            raise Tripoli2ApiException(e.fault.detail.errorResponse.errors.error.message)