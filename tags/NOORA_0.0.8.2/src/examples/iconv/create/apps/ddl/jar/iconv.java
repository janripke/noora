create or replace and compile java source named iconv as
package com.twoorganize.kpn;

import java.io.*;
import java.util.*;

public class IConv {

  
  private static String readFile(String url, String charset) throws Exception {
	StringBuffer buffer = new StringBuffer();
    
    FileInputStream fis = new FileInputStream(url);
    InputStreamReader isr = new InputStreamReader(fis, charset);
    Reader in = new BufferedReader(isr);
    int ch;
    while ((ch = in.read()) > -1) {
      buffer.append((char)ch);
    }
    in.close();
    return buffer.toString();     
  }
    
    
  private static void writeFile(String url, String content, String charset) throws Exception {
    FileOutputStream fos = new FileOutputStream(url);
    Writer out = new OutputStreamWriter(fos, charset);
    out.write(content);
    out.close();
  }

  
  public static void convert(String url, String sourceCharset, String targetCharset) throws Exception {

    try {
      File f = new File(url);
      Properties prop = new Properties(System.getProperties());
      prop.setProperty("user.dir",f.getAbsolutePath() );
      System.setProperties(prop); 

      String content = readFile(url,sourceCharset);
      writeFile(url,content,targetCharset);
    }
    catch (Exception e) {
      throw e;
    }
  }  

  
}
/

