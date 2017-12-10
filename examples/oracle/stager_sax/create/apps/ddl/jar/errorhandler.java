create or replace and compile java source named errorhandler as
package com.twoorganize.kpn;

import org.xml.sax.SAXParseException;
import org.xml.sax.SAXException;


// vanuit het aanroepende oracle package kan worden
// bepaald of er wordt gecommit of dat er een rollback wordt gegeven.
public class ErrorHandler extends ContentFormatter {
  
  public void error(SAXParseException exception) {
    this.parsed=false;
    this.parseException = exception;
  }
  
  public void fatalError(SAXParseException exception) {
    this.parsed=false;
    this.parseException = exception;
  }
  
  public void warning(SAXParseException exception) {
    this.parsed=false;
    this.parseException = exception;
  }
  
  
}
/
