class TripolisDirectEmail:
    # def __init__(self, directEmailId = None, label = None, name = None, subject = None, description = None, fromName = None, fromAddress = None, replyTo = None, html = None, text = None):
    """
    'data' Is a string containing python script. It must declare all attributes of the class. I.e.:

    directEmailId = None
    label = '09_invite_new_user'
    name = '09_invite_new_user'
    subject = 'Aanmelding FLITS helpdesk applicatie'
    description = None
    fromName = 'KPN'
    fromAddress = 'publicaties@emailservice-kpn.com'
    replyTo = None

    html = \"""
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"><html>
    <head>

    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    </head>
    <body>
    Geachte gebruiker,<br/>
    <br/>
    Er is een account voor u aangemaakt voor de FILTS helpdeskapplicatie.<br/>
    Klik op onderstaande link om uw gegevens in te stellen:<br/>
    <a href="http://192.168.36.6:9000/#/invite/${contact.user_invite_key!}">Vul hier uw gegevens in</a><br/>
    <br/>
    Met vriendelijk groet,<br/>
    FLITS beheerteam
    </body>
    </html>
    \"""

    text = \"""
    <#assign nu = .now>
    U heeft een e-mail ontvangen in HTML-formaat, maar uw e-mailprogramma ondersteunt geen HTML.
    Klik op onderstaande link om de e-mail in uw browser te lezen.
    [view_online=webversie]

    copyright ${nu?string.yyyy} KPN
    \"""
    """
    def __init__(self, data):
        exec (data)

        try:
            label
            subject
            description
            fromName
            fromAddress
            replyTo
            html
            text
        except NameError:
            raise
        else:
            self.__label = label
            self.__name = name
            self.__subject = subject
            self.__description = description
            self.__fromName = fromName
            self.__fromAddress = fromAddress
            self.__replyTo = replyTo
            self.__html = html
            self.__text = text

    def getLabel(self):
        return self.__label

    def setLabel(self, value):
        self.__label = value

    def getName(self):
        return self.__name

    def setName(self, value):
        self.__name = value

    def getSubject(self):
        return self.__subject

    def setSubject(self, value):
        self.__subject = value

    def getDescription(self):
        return self.__description

    def setDescription(self, value):
        self.__description = value

    def getFromName(self):
        return self.__fromName

    def setFromName(self, value):
        self.__fromName = value

    def getFromAddress(self):
        return self.__fromAddress

    def setFromAddress(self, value):
        self.__fromAddress = value

    def getReplyTo(self):
        return self.__replyTo

    def setReplyTo(self, value):
        self.__replyTo = value

    def getHtml(self):
        return self.__html

    def setHtml(self, value):
        self.__html = value

    def getText(self):
        return self.__text

    def setText(self, value):
        self.__text = value

    def __str__(self):
        return "label=%s, name=%s, subject=%s, description=%s, fromName=%s, fromAddress=%s, replyTo=%s, html=%s, text=%s" % (
            self.__label, self.__name, self.__subject, self.__description, self.__fromName, self.__fromAddress, self.__replyTo,
            self.__html, self.__text)
