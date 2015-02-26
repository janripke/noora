create or replace and compile java source named saxprocessor as
package com.twoorganize.kpn;

import java.io.StringReader;
import java.util.ArrayList;

import org.xml.sax.InputSource;
import org.xml.sax.SAXParseException;

import oracle.xml.parser.v2.SAXParser;
import oracle.xml.parser.v2.XMLDocument;
import oracle.xml.parser.schema.*;
import oracle.sql.BFILE;
import oracle.xdb.XMLType;


public class SaxProcessor {

  private static int getColumnCount(String value, String delimiter) {
    String[] values = value.split(delimiter);
    return values.length;
  }

  
  private static String getColumn(String value, String delimiter, int column) {
    String[] values = value.split(delimiter);
    if (column < values.length) {
      return values[column];
    }
    return null;
  }
  
  private static ArrayList stringToArrayList(String elements, String delimiter) {
    ArrayList result = new ArrayList();
    int count = getColumnCount(elements,delimiter);
    for (int i=0; i < count ; i++) {
      String elementValue = getColumn(elements,delimiter,i);
        if (elementValue!=null && !"".equals(elementValue)) {
          result.add(elementValue);
        }
    }
    return result;
  }

  public static int parse(BFILE bfile, String jobName, String contentHandlerName, String tableName, String errorTableName, String xmlTableName, String rootElements, String childElements, String sourceCharset, String targetCharset) throws Exception {

    try {

      ContentFormatter contentHandler = (ContentFormatter)Class.forName(contentHandlerName).newInstance();
      contentHandler.setJobName(jobName);
      contentHandler.setTableName(tableName);
      contentHandler.setErrorTableName(errorTableName);
      contentHandler.setXmlTableName(xmlTableName);
      contentHandler.setRootElements(stringToArrayList(rootElements,","));
      contentHandler.setChildElements(stringToArrayList(childElements,","));                  
      contentHandler.setSourceCharset(sourceCharset);
      contentHandler.setTargetCharset(targetCharset);    

      SAXParser parser = new SAXParser();
      parser.setAttribute(SAXParser.STANDALONE, Boolean.valueOf(true));      
      parser.setValidationMode(SAXParser.NONVALIDATING);
      parser.setContentHandler(contentHandler);
      
      bfile.openFile();
      parser.parse(bfile.getBinaryStream());
      bfile.closeFile();
      return contentHandler.getRowCount();
    }
    catch (Exception e) {
      throw e;
    }
  }
  
  private static void failOnParseException(ContentFormatter errorHandler) throws SAXParseException {
    if (!errorHandler.isValid()) {
       throw errorHandler.getParseException();
    }
  }
  
  public static void validate(BFILE bfile, String jobName, String errorHandlerName, XMLType schema) throws Exception {
    try {
    
      ContentFormatter errorHandler = (ContentFormatter)Class.forName(errorHandlerName).newInstance();
      errorHandler.setJobName(jobName);
      
      SAXParser parser = new SAXParser();
      parser.setValidationMode(SAXParser.SCHEMA_VALIDATION);
      parser.setAttribute(SAXParser.STANDALONE, Boolean.valueOf(true));  

      XSDBuilder builder = new XSDBuilder();
                 
      String doc=schema.getStringVal();
      StringReader stringReader = new StringReader(doc);
      InputSource inputSource = new InputSource(stringReader);
      XMLSchema xmlSchema = builder.build(inputSource);            
      parser.setXMLSchema(xmlSchema);
      parser.setErrorHandler(errorHandler);
            
      bfile.openFile();
      parser.parse(bfile.getBinaryStream());
      bfile.closeFile();
      failOnParseException(errorHandler);
    }
    catch (Exception e) {
      throw e;
    }
  }
  
}
/

