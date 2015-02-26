create or replace and compile java source named contentformatter as
package com.twoorganize.kpn;

import org.xml.sax.helpers.DefaultHandler;
import org.xml.sax.SAXParseException;
import java.util.ArrayList;

abstract class ContentFormatter extends DefaultHandler {

  protected String            jobName;
  protected String            schemaName;
  protected String            tableName;
  protected String            errorTableName;
  protected String            xmlTableName;
  protected ArrayList         rootElements;
  protected ArrayList         childElements;
  protected int               rowCount=0;
  protected boolean           parsed = true;
  protected SAXParseException parseException;
  protected String            sourceCharset;
  protected String            targetCharset;
  
  
  public boolean isValid() {
    return this.parsed;
  }
  

  public SAXParseException getParseException() {
    return this.parseException;
  }
 
  
  protected int getRowCount() {
    return this.rowCount;
  }
  

  protected void setJobName(String jobName) {
    this.jobName = jobName;
  }


  protected void setSchemaName(String schemaName) {
    this.schemaName = schemaName;
  }

  
  protected void setTableName(String tableName) {
    this.tableName = tableName;
  }
  
  
  protected void setErrorTableName(String errorTableName) {
    this.errorTableName = errorTableName;
  }
  
  
  protected void setXmlTableName(String xmlTableName) {
    this.xmlTableName = xmlTableName;
  }
  
  protected void setRootElements(ArrayList rootElements) {
    this.rootElements = rootElements;
  }
  
  
  protected void setChildElements(ArrayList childElements) {
    this.childElements = childElements;
  }

  protected void setSourceCharset(String sourceCharset) {
    this.sourceCharset = sourceCharset;
  }

  protected void setTargetCharset(String targetCharset) {
    this.targetCharset = targetCharset;
  }
  
}
/

