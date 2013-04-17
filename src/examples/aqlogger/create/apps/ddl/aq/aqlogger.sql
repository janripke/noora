begin
  -- Queue table for messages
  dbms_aqadm.create_queue_table
    (queue_table        => 'QT_AQLOGGER',
     queue_payload_type => 'sys.aq$_jms_text_message',
     sort_list          => 'ENQ_TIME',
     Compatible         => '10.2.0',
     multiple_consumers => true); 
                                                            
  -- Create the queue
  dbms_aqadm.create_queue
    (queue_name     => 'AQLOGGER',
     queue_table    => 'QT_AQLOGGER',
     queue_type     => sys.dbms_aqadm.normal_queue,
     retry_delay    => 600,         -- Na 10 minuten is het beschikbaar voor nieuwe poging
     retention_time => 5 * 24 * 60 * 60, -- Houd berichten op OTA 5 dagen vast voor testdoeleinden
     max_retries    => 3
  );
  -- dbms_aqadm.grant_type_access('APPS');  

                           
   -- start the queue
   dbms_aqadm.start_queue( queue_name =>'AQLOGGER' , enqueue => true ,dequeue => true );
   --
   dbms_aqadm.start_queue('AQ$_QT_AQLOGGER_E',false,true);
end;
/
