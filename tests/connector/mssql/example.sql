CREATE TABLE customer
	([customerid] int, [custtype] varchar(4))
;

INSERT INTO customer
	([customerid], [custtype])
VALUES
	(1, 'test'),
	(2, 'blah')
;

CREATE TABLE [order]
	([ordernumber] int, [customerid] int)
;

INSERT INTO [order]
	([ordernumber], [customerid])
VALUES
	(10636909, 1),
	(10254, 2)
;

CREATE FUNCTION getCustomerType (@orderNumber INT)
    RETURNS VARCHAR(30)
AS
begin
  return (select custtype
                      from Customer c
                      join [order] o
                        on o.customerid =  c.customerid
                      where o.orderNumber = @orderNumber)
end
