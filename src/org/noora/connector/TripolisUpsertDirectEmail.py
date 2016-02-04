from suds.client import Client
from suds.multipart import MultipartFilter


class TripolisUpsertDirectEmail:
    def __init__(self, url, client, username, password, workspace, direct_email_type, tripolis_direct_email):
        self.__client = Client(url, plugins=[MultipartFilter()])

        self.__auth_info = self.__client.factory.create('AuthInfo')
        self.__auth_info.client = client
        self.__auth_info.username = username
        self.__auth_info.password = password

        self.__workspace = workspace
        self.__direct_email_type = direct_email_type

        self.__direct_email = self.__client.factory.create('DirectEmail')
        self.__direct_email.label = tripolis_direct_email.getLabel()
        self.__direct_email.name = tripolis_direct_email.getName()
        self.__direct_email.subject = tripolis_direct_email.getSubject()
        self.__direct_email.description = tripolis_direct_email.getDescription()
        self.__direct_email.fromName = tripolis_direct_email.getFromName()
        self.__direct_email.fromAddress = tripolis_direct_email.getFromAddress()
        self.__direct_email.replyTo = tripolis_direct_email.getReplyTo()
        self.__direct_email.html = tripolis_direct_email.getHtml()
        self.__direct_email.text = tripolis_direct_email.getText()
        self.findDirectEmailId()

    def findDirectEmailId(self):
        direct_emails = self.__client.service.getDirectEmails(authInfo=self.__auth_info, workspaceName=self.__workspace,
                                       emailTypeDefinitionName=self.__direct_email_type, includeContent=False)

        for direct_email in direct_emails:
            if direct_email.label == self.__direct_email.label:
                self.__direct_email.directEmailId = direct_email.directEmailId
                return

    def upsert(self):
        return self.__client.service.upsertDirectMail(authInfo=self.__auth_info, workspaceName=self.__workspace,
                                               directEmailTypeName=self.__direct_email_type,
                                               directEmail=self.__direct_email)
