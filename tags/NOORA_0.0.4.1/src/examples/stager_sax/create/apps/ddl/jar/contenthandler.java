create or replace and compile java source named hkppcontenthandler as
package com.twoorganize.kpn;

import java.io.IOException;
import java.io.StringWriter;

import java.io.Writer;
import java.io.*;

import java.nio.charset.Charset;
import java.nio.charset.CharsetDecoder;
import java.nio.charset.CharsetEncoder;
import java.nio.charset.CharacterCodingException;
import java.nio.CharBuffer;
import java.nio.ByteBuffer;


import java.sql.DriverManager;
import java.sql.SQLException;

import java.util.Enumeration;
import java.util.Hashtable;
import java.util.ArrayList;
import java.util.HashMap;

import oracle.jdbc.OracleConnection;
import oracle.jdbc.OracleDriver;

import oracle.jdbc.OraclePreparedStatement;
import oracle.jdbc.OracleCallableStatement;

import oracle.sql.BFILE;
import oracle.sql.CLOB;
import oracle.xdb.XMLType;

import oracle.xml.parser.v2.SAXParser;
import oracle.xml.parser.v2.XMLDocument;
import oracle.xml.parser.v2.XMLElement;
import oracle.xml.parser.v2.XMLNode;

//import org.w3c.dom.Attr;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.Text;


import org.xml.sax.Attributes;
import org.xml.sax.ContentHandler;
import org.xml.sax.Locator;
import org.xml.sax.SAXException;

// vanuit het aanroepende oracle package kan worden
// bepaald of er wordt gecommit of dat er een rollback wordt gegeven.
public class HKPPContentHandler extends ContentFormatter {

  private static final char M_LF  = 10;	
	
  private int rowId = 0;

  private String                  currentElement;
  private OracleConnection        conn;
  
  private Hashtable               elementValues = new Hashtable();
  private Hashtable               elements = new Hashtable();
  private HashMap                 parentElements = new HashMap();  
  private String                  document = "";

  
  private void connect() throws SQLException {
    DriverManager.registerDriver(new oracle.jdbc.OracleDriver());
    OracleDriver ora = new OracleDriver();
    this.conn = (OracleConnection)ora.defaultConnection();
  }


  private void logger(String jobName, String packageName, String methodName, String message) throws SAXException {

    try {    
      String sqlStatement = "begin logger.debug(?,?,?,?); end;";
      OracleCallableStatement cs = (OracleCallableStatement)conn.prepareCall (sqlStatement);
      cs.setString("p_job_name", jobName);
      cs.setString("p_package_name", packageName);
      cs.setString("p_method_name", methodName);
      cs.setString("p_message", message);
      cs.execute();
      cs.close();
    }
    catch (SQLException sqlE) {
      throw new SAXException(sqlE);
    }
  }
  
  
  private String getCurrentElement() {
    return this.currentElement;
  }
  
  
  private void setCurrentElement (String value) {
    if (this.currentElement == null) {
      this.currentElement = value;
    } else {
      this.currentElement = this.currentElement + "." + value;
    }
  }

  
  private void addElement (String key, String value) {
    if (!this.elements.containsKey(key)) {
      this.elements.put(key,value);
    }
  }
  
  
  private void addParentElement(String key, String value) {
    if (!this.parentElements.containsKey(key)) {
      this.parentElements.put(key, value);
    }
  }
    
  private Hashtable getElementValues(String key) {
	Hashtable result = new Hashtable();
	Enumeration keys = this.elementValues.keys();
	while( keys.hasMoreElements() ) {
	  String keyElement = (String)keys.nextElement();
	  if (keyElement.startsWith(key+'.')) {
	    result.put(keyElement,this.elementValues.get(keyElement));
	    this.elementValues.remove(keyElement);
	  }
	}
	return result;
  }
	  
	  
  private String getSqlString(String value) {
    return "'" + value + "'";
  }
	  
	  
  private int getElementTypeId(String name) {
    if (this.rootElements.contains(name)) {
      return this.rootElements.indexOf(name);
    } 
    if (this.childElements.contains(name)) {
      return (this.childElements.indexOf(name)+1)*100;
    }
    return -1;
  }
	

  private String decode(String value, String sourceCharset, String targetCharset) throws CharacterCodingException {
    // UTF-8
    // ISO-8859-1

    Charset utf8Charset = Charset.forName(sourceCharset);
    Charset latin1Charset = Charset.forName(targetCharset);
    CharsetDecoder decoder = latin1Charset.newDecoder(); 
    CharsetEncoder encoder = utf8Charset.newEncoder(); 
    ByteBuffer bbuf = encoder.encode(CharBuffer.wrap(value));
    CharBuffer cbuf = decoder.decode(bbuf); 
    return cbuf.toString();
  }



  private void insertDocument(String jobName, int rowId, String type, String document, String tableName) throws SQLException {

        String sqlStatement = "INSERT INTO " + tableName + "(job_name, row_id, content, type, type_id) VALUES (?,?,?,?,?)";
      	int typeId = getElementTypeId(type);	

        OraclePreparedStatement ps=(OraclePreparedStatement) conn.prepareStatement(sqlStatement);
      	ps.setString(1,jobName);
       	ps.setInt(2,rowId);
      	ps.setString(3,this.document);
	      ps.setString(4,type);
        ps.setInt(5,typeId);
	      ps.execute();
        ps.close();

  }

  
	  
  private void insertElement(String jobName, int rowId, String type, String tableName, String errorTableName) throws SQLException {

    int typeId = getElementTypeId(type);
    String sqlFields = "job_name, row_id, type, type_id";
    String sqlValueParameters = "?,?,?,?";
    String sqlLog = " log errors into " + errorTableName + " reject limit 0";     
	    
    Hashtable values = getElementValues(this.currentElement);
    Enumeration keys = values.keys();
    while(keys.hasMoreElements()) {
      String key = (String)keys.nextElement();
      String value = (String)values.get(key);
      String fieldName = (String)this.elements.get(key);                
      sqlFields = sqlFields + "," + fieldName;
      sqlValueParameters = sqlValueParameters + ",?";
    }

    String sqlStatement = "INSERT INTO " + tableName + " (" + sqlFields + ") VALUES (" + sqlValueParameters + ")" + sqlLog;
    OraclePreparedStatement ps=(OraclePreparedStatement) conn.prepareStatement(sqlStatement);
    ps.setString(1,this.jobName);
    ps.setInt(2,this.rowId);
	  ps.setString(3,type);
    ps.setInt(4,typeId);

    keys = values.keys();
    int i = 5;
    while(keys.hasMoreElements()) {
      String key = (String)keys.nextElement();
      String value = (String)values.get(key);
      ps.setString(i,value);    
      i = i + 1;
    }
    
    ps.execute();
    ps.close();

  }
  
  
  public void startElement(String namespaceURI, String localName, String elementName, Attributes attrs) throws SAXException {

    String parentElement = this.currentElement;
    setCurrentElement(localName);
    addElement(this.currentElement,localName);
    addParentElement(this.currentElement,parentElement);

    
    if (this.rootElements.contains(this.currentElement)) {
      this.document = "";
    }
    this.document = this.document + ("<"+localName+">"); 
  }

  

  public void endElement(String namespaceURI, String localName, String qName) throws SAXException {
  
	this.document = this.document + ("</"+localName+">") + M_LF; 
    try {
          	          
      if (this.rootElements.contains(this.currentElement)) { 

        insertElement(this.jobName,this.rowId,this.currentElement,this.tableName,this.errorTableName);
        insertDocument(this.jobName,this.rowId,this.currentElement,this.document,this.xmlTableName);
        this.rowCount=this.rowCount + 1;
        
        this.elementValues.clear();
        this.rowId = this.rowId + 1;          
      } else if (this.childElements.contains(this.currentElement)) {
        insertElement(jobName,rowId,currentElement,tableName,errorTableName);
      }
    }
    catch (SQLException sqlE) {
      throw new SAXException(sqlE);
    }
    
    this.currentElement = (String)this.parentElements.get(this.currentElement);
    
  }


  public void characters(char[] p0, int p1, int p2) throws SAXException {
    try {
      StringWriter sw = new StringWriter();
      sw.write(p0, p1, p2);
      String value = decode(sw.toString().trim(),this.sourceCharset,this.targetCharset);    
      if (value != null && !"".equals(value)) {
        elementValues.put(currentElement,value);
        this.document = this.document + value;
      }
    }
    catch (CharacterCodingException cce) {
      throw new SAXException(cce);
    }


  }


  public void startDocument() throws SAXException {
    try {      
      connect();
    }
    catch (SQLException sqlE) {
      throw new SAXException(sqlE);
    }

  }

  public void endDocument() throws SAXException {
  }

  public void startPrefixMapping(String prefix, String uri) throws SAXException {
  }

  public void endPrefixMapping(String prefix) throws SAXException {
  }

  public void ignorableWhitespace(char[] p0, int p1, int p2) throws SAXException {
  }

  public void processingInstruction(String p0, String p1) throws SAXException {
    throw new SAXException("processingInstruction not implemented.");
  }

  public void setDocumentLocator(Locator p0) {
    // throw new SAXException ("Un-Implemented Method: setDocumentLocator");
  }

  public void skippedEntity(String p0) throws SAXException {
    throw new SAXException("skippedEntity not implemented.");
  }
  
}
/

