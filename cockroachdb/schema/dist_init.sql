CREATE DATABASE IF NOT EXISTS a_dist;
USE a_dist;

DROP TABLE IF EXISTS Warehouse_Read, Warehouse_Write, District_Read, District_Write, 
Customer_Read, Customer_Write, Customer_Misc, Order_Read, Order_Write, Item_Read, 
Item_Misc, OrderLine_Read, OrderLine_Write, Stock_Write, Stock_Misc;

CREATE TABLE Warehouse_Read (
    W_ID INTEGER, 
    W_NAME VARCHAR(10), 
    W_STREET_1 VARCHAR(20), 
    W_STREET_2 VARCHAR(20), 
    W_CITY VARCHAR(20), 
    W_STATE CHAR(2), 
    W_ZIP CHAR(9), 
    W_TAX DECIMAL(4, 4), 
    PRIMARY KEY (W_ID)
);

CREATE TABLE Warehouse_Write (
    W_ID INTEGER, 
    W_YTD DECIMAL(12, 2), 
    PRIMARY KEY (W_ID)
);

CREATE TABLE District_Read (
    D_W_ID INTEGER, 
    D_ID INTEGER, 
    D_STREET_1 VARCHAR(20), 
    D_STREET_2 VARCHAR(20), 
    D_CITY VARCHAR(20), 
    D_STATE CHAR(2), 
    D_ZIP CHAR(9), 
    D_TAX DECIMAL(4, 4), 
    PRIMARY KEY (D_W_ID, D_ID), 
    FOREIGN KEY (D_W_ID) REFERENCES Warehouse_Read(W_ID)
);

CREATE TABLE District_Write (
    D_W_ID INTEGER, 
    D_ID INTEGER, 
    D_YTD DECIMAL(12, 2), 
    D_NEXT_O_ID INTEGER, 
    PRIMARY KEY (D_W_ID, D_ID), 
    FOREIGN KEY (D_W_ID) REFERENCES Warehouse_Read(W_ID)
);

CREATE TABLE Customer_Read (
    C_W_ID INTEGER, 
    C_D_ID INTEGER, 
    C_ID INTEGER, 
    C_FIRST VARCHAR(16), 
    C_MIDDLE CHAR(2), 
    C_LAST VARCHAR(16), 
    C_STREET_1 VARCHAR(20), 
    C_STREET_2 VARCHAR(20), 
    C_CITY VARCHAR(20), 
    C_STATE CHAR(2), 
    C_ZIP CHAR(9), 
    C_PHONE CHAR(16), 
    C_SINCE TIMESTAMP, 
    C_CREDIT CHAR(2), 
    C_CREDIT_LIM DECIMAL(12, 2), 
    C_DISCOUNT DECIMAL(4, 4), 
    PRIMARY KEY (C_W_ID, C_D_ID, C_ID), 
    FOREIGN KEY (C_W_ID, C_D_ID) REFERENCES District_Read(D_W_ID, D_ID)
);

CREATE TABLE Customer_Write (
    C_W_ID INTEGER, 
    C_D_ID INTEGER, 
    C_ID INTEGER, 
    C_BALANCE DECIMAL(12, 2), 
    C_YTD_PAYMENT FLOAT, 
    C_PAYMENT_CNT INT, 
    C_DELIVERY_CNT INT, 
    PRIMARY KEY (C_W_ID, C_D_ID, C_ID), 
    FOREIGN KEY (C_W_ID, C_D_ID) REFERENCES District_Read(D_W_ID, D_ID)
);

CREATE TABLE Customer_Misc (
    C_W_ID INTEGER, 
    C_D_ID INTEGER, 
    C_ID INTEGER,
    C_DATA VARCHAR(500), 
    PRIMARY KEY (C_W_ID, C_D_ID, C_ID), 
    FOREIGN KEY (C_W_ID, C_D_ID) REFERENCES District_Read(D_W_ID, D_ID)
);

CREATE TABLE Order_Read (
    O_W_ID INTEGER, 
    O_D_ID INTEGER, 
    O_ID INTEGER, 
    O_C_ID INTEGER, 
    O_OL_CNT DECIMAL(2, 0), 
    O_ALL_LOCAL DECIMAL(1, 0), -- True or False 
    O_ENTRY_ID TIMESTAMP, 
    PRIMARY KEY (O_W_ID, O_D_ID, O_ID), 
    FOREIGN KEY (O_W_ID, O_D_ID, O_C_ID) REFERENCES Customer_Read(C_W_ID, C_D_ID, C_ID)
);

CREATE TABLE Order_Write (
    O_W_ID INTEGER, 
    O_D_ID INTEGER, 
    O_ID INTEGER, 
    O_C_ID INTEGER, 
    O_CARRIER_ID INTEGER, -- Create Index? Care of NULL
    PRIMARY KEY (O_W_ID, O_D_ID, O_ID), 
    FOREIGN KEY (O_W_ID, O_D_ID, O_C_ID) REFERENCES Customer_Read(C_W_ID, C_D_ID, C_ID),
    CHECK (O_CARRIER_ID >= 1 AND O_CARRIER_ID <= 10)
);

CREATE TABLE Item_Read (
    I_ID INTEGER, 
    I_NAME VARCHAR(24), 
    I_PRICE DECIMAL(5, 2), 
    PRIMARY KEY (I_ID)
);

CREATE TABLE Item_Misc (
    I_ID INTEGER, 
    I_IM_ID INTEGER, 
    I_DATA VARCHAR(50), 
    PRIMARY KEY (I_ID)
);

CREATE TABLE OrderLine_Read (
    OL_W_ID INTEGER, 
    OL_D_ID INTEGER,
    OL_O_ID INTEGER,
    OL_NUMBER INTEGER, 
    OL_I_ID INTEGER, 
    OL_AMOUNT DECIMAL(6, 2), 
    OL_SUPPLY_W_ID INTEGER, 
    OL_QUANTITY DECIMAL(2, 0), 
    OL_DIST_INFO CHAR(24),
    PRIMARY KEY (OL_W_ID, OL_D_ID, OL_O_ID, OL_NUMBER), 
    FOREIGN KEY (OL_W_ID, OL_D_ID, OL_O_ID) REFERENCES Orders(O_W_ID, O_D_ID, O_ID),
    FOREIGN KEY (OL_I_ID) REFERENCES Item_Read(I_ID)
);

CREATE TABLE OrderLine_Write (
    OL_W_ID INTEGER, 
    OL_D_ID INTEGER,
    OL_O_ID INTEGER,
    OL_NUMBER INTEGER, 
    OL_I_ID INTEGER, 
    OL_DELIVERY_D TIMESTAMP, 
    PRIMARY KEY (OL_W_ID, OL_D_ID, OL_O_ID, OL_NUMBER), 
    FOREIGN KEY (OL_W_ID, OL_D_ID, OL_O_ID) REFERENCES Orders(O_W_ID, O_D_ID, O_ID),
    FOREIGN KEY (OL_I_ID) REFERENCES Item_Read(I_ID)
);

CREATE TABLE Stock_Write (
    S_W_ID INTEGER, 
    S_I_ID INTEGER, 
    S_QUANTITY DECIMAL(4, 0), 
    S_YTD DECIMAL(8, 2), 
    S_ORDER_CNT INTEGER, 
    S_REMOTE_CNT INTEGER, 
    PRIMARY KEY (S_W_ID, S_I_ID), 
    FOREIGN KEY (S_W_ID) REFERENCES Warehouse_Read(W_ID),
    FOREIGN KEY (S_I_ID) REFERENCES Item_Read(I_ID)
);

CREATE TABLE Stock_Misc (
    S_W_ID INTEGER, 
    S_I_ID INTEGER, 
    S_DIST_01 CHAR(24), 
    S_DIST_02 CHAR(24), 
    S_DIST_03 CHAR(24),
    S_DIST_04 CHAR(24), 
    S_DIST_05 CHAR(24), 
    S_DIST_06 CHAR(24), 
    S_DIST_07 CHAR(24), 
    S_DIST_08 CHAR(24), 
    S_DIST_09 CHAR(24), 
    S_DIST_10 CHAR(24),
    S_DATA VARCHAR(50), 
    PRIMARY KEY (S_W_ID, S_I_ID), 
    FOREIGN KEY (S_W_ID) REFERENCES Warehouse_Read(W_ID),
    FOREIGN KEY (S_I_ID) REFERENCES Item_Read(I_ID)
);

-- run `cd seed/ && python3 -m http.server 3000` in xcnd36

IMPORT INTO Warehouse_Read CSV DATA ('http://xcnd36:3000/dist_data_files/warehouse_read_headers.csv') WITH nullif = 'null';
IMPORT INTO Warehouse_Write CSV DATA ('http://xcnd36:3000/dist_data_files/warehouse_write_headers.csv') WITH nullif = 'null';

IMPORT INTO District_Read CSV DATA ('http://xcnd36:3000/dist_data_files/district_read_headers.csv') WITH nullif = 'null';
IMPORT INTO District_Write CSV DATA ('http://xcnd36:3000/dist_data_files/district_write_headers.csv') WITH nullif = 'null';

IMPORT INTO Customer_Read CSV DATA ('http://xcnd36:3000/dist_data_files/customer_read_headers.csv') WITH nullif = 'null';
IMPORT INTO Customer_Write CSV DATA ('http://xcnd36:3000/dist_data_files/customer_write_headers.csv') WITH nullif = 'null';
IMPORT INTO Customer_Misc CSV DATA ('http://xcnd36:3000/dist_data_files/customer_misc_headers.csv') WITH nullif = 'null';

IMPORT INTO Order_Read CSV DATA ('http://xcnd36:3000/dist_data_files/order_read_headers.csv') WITH nullif = 'null';
IMPORT INTO Order_Write CSV DATA ('http://xcnd36:3000/dist_data_files/order_write_headers.csv') WITH nullif = 'null';

IMPORT INTO Item_Read CSV DATA ('http://xcnd36:3000/dist_data_files/item_read_headers.csv') WITH nullif = 'null';
IMPORT INTO Item_Misc CSV DATA ('http://xcnd36:3000/dist_data_files/item_misc_headers.csv') WITH nullif = 'null';

IMPORT INTO OrderLine_Read CSV DATA ('http://xcnd36:3000/dist_data_files/order_line_read_headers.csv') WITH nullif = 'null';
IMPORT INTO OrderLine_Write CSV DATA ('http://xcnd36:3000/dist_data_files/order_line_write_headers.csv') WITH nullif = 'null';

IMPORT INTO Stock_Write CSV DATA ('http://xcnd36:3000/dist_data_files/stock_write_headers.csv') WITH nullif = 'null';
IMPORT INTO Stock_Misc CSV DATA ('http://xcnd36:3000/dist_data_files/stock_misc_headers.csv') WITH nullif = 'null';
