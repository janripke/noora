<%@ taglib uri="/WEB-INF/struts-html" prefix="html" %>

<html:html>
<head>
	<title>KickStart: Input name</title>
</head>
<body>
    <html:form action="/greeting.do">
        <table border="0" cellspacing="0" cellpadding="0">
            <tr>
                <td><b>Input name:</b></td>
            </tr>
            <tr>
                <td>
                    <html:text property="name" />
                    <html:submit value="   Say Hello!   " />
                </td>
            </tr>
        </table>
    </html:form>
</body>
</html:html>
