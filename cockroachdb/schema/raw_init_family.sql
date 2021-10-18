DROP DATABASE IF EXISTS a_raw;
CREATE DATABASE IF NOT EXISTS a_raw;
USE a_raw;

-- DROP TABLE IF EXISTS Stock, OrderLine, Item, Orders, Customer, District, Warehouse;

CREATE TABLE IF NOT EXISTS Warehouse (
    W_ID INTEGER,
    W_NAME VARCHAR(10),
    W_STREET_1 VARCHAR(20),
    W_STREET_2 VARCHAR(20),
    W_CITY VARCHAR(20),
    W_STATE CHAR(2),
    W_ZIP CHAR(9),
    W_TAX DECIMAL(4, 4),
    W_YTD DECIMAL(12, 2),
    PRIMARY KEY (W_ID),
    FAMILY f1 (W_ID, W_YTD),
    FAMILY f2 (W_NAME, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP, W_TAX)
);

CREATE TABLE IF NOT EXISTS District (
    D_W_ID INTEGER,
    D_ID INTEGER,
    D_NAME VARCHAR(10),
    D_STREET_1 VARCHAR(20),
    D_STREET_2 VARCHAR(20),
    D_CITY VARCHAR(20),
    D_STATE CHAR(2),
    D_ZIP CHAR(9),
    D_TAX DECIMAL(4, 4),
    D_YTD DECIMAL(12, 2),
    D_NEXT_O_ID INTEGER,
    PRIMARY KEY (D_W_ID, D_ID),
    FOREIGN KEY (D_ID) REFERENCES Warehouse(W_ID),
    FAMILY f1 (D_W_ID, D_ID, D_YTD, D_NEXT_O_ID),
    FAMILY f2 (D_NAME, D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP, D_TAX)
);

CREATE TABLE IF NOT EXISTS Customer (
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
    C_BALANCE DECIMAL(12, 2),
    C_YTD_PAYMENT FLOAT,
    C_PAYMENT_CNT INT,
    C_DELIVERY_CNT INT,
    C_DATA VARCHAR(500),
    PRIMARY KEY (C_W_ID, C_D_ID, C_ID),
    FOREIGN KEY (C_W_ID, C_D_ID) REFERENCES District(D_W_ID, D_ID),
    FAMILY f1 (C_W_ID, C_D_ID, C_ID, C_BALANCE, C_YTD_PAYMENT, C_PAYMENT_CNT, C_DELIVERY_CNT),
    FAMILY f2 (C_FIRST, C_MIDDLE, C_LAST, C_STREET_1, C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM, C_DISCOUNT, C_DATA)
);

CREATE TABLE IF NOT EXISTS Orders (
    id UUID NOT NULL PRIMARY KEY DEFAULT gen_random_uuid() , -- spread orders more evenly
    O_W_ID INTEGER NOT NULL,
    O_D_ID INTEGER NOT NULL,
    O_ID INTEGER NOT NULL,
    O_C_ID INTEGER,
    O_CARRIER_ID INTEGER,
    O_OL_CNT DECIMAL(2, 0),
    O_ALL_LOCAL DECIMAL(1, 0), -- True or False
    O_ENTRY_D TIMESTAMP,
    UNIQUE (O_W_ID, O_D_ID, O_ID ASC),
    FOREIGN KEY (O_W_ID, O_D_ID, O_C_ID) REFERENCES Customer(C_W_ID, C_D_ID, C_ID)
);

CREATE TABLE IF NOT EXISTS Carrier (
    id PRIMARY KEY, 
    O_CARRIER_ID  
) AS
SELECT id, O_CARRIER_ID FROM Orders; 

CREATE TABLE IF NOT EXISTS Item (
    I_ID INTEGER PRIMARY KEY,
    I_NAME VARCHAR(24),
    I_PRICE DECIMAL(5, 2),
    I_IM_ID INTEGER,
    I_DATA VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS OrderLine (
    OL_W_ID INTEGER,
    OL_D_ID INTEGER,
    OL_O_ID INTEGER,
    OL_NUMBER INTEGER,
    OL_I_ID INTEGER,
    OL_DELIVERY_D TIMESTAMP,
    OL_AMOUNT DECIMAL(7, 2),
    OL_SUPPLY_W_ID INTEGER,
    OL_QUANTITY DECIMAL(2, 0),
    OL_DIST_INFO CHAR(24),
    PRIMARY KEY (OL_W_ID, OL_D_ID, OL_O_ID, OL_NUMBER),
    FOREIGN KEY (OL_W_ID, OL_D_ID, OL_O_ID) REFERENCES Orders(O_W_ID, O_D_ID, O_ID),
    FOREIGN KEY (OL_I_ID) REFERENCES Item(I_ID)
);

CREATE TABLE IF NOT EXISTS Stock (
    S_W_ID INTEGER,
    S_I_ID INTEGER,
    S_QUANTITY DECIMAL(4, 0),
    S_YTD DECIMAL(8, 2),
    S_ORDER_CNT INTEGER,
    S_REMOTE_CNT INTEGER,
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
    FOREIGN KEY (S_W_ID) REFERENCES Warehouse(W_ID),
    FOREIGN KEY (S_I_ID) REFERENCES Item(I_ID),
    FAMILY f1 (S_W_ID, S_I_ID, S_QUANTITY, S_YTD, S_ORDER_CNT, S_REMOTE_CNT),
    FAMILY f2 (S_DIST_01, S_DIST_02, S_DIST_03, S_DIST_04, S_DIST_05, S_DIST_06, S_DIST_07, S_DIST_08, S_DIST_09, S_DIST_10, S_DATA)
);

-- run `cd seed/ && python3 -m http.server 3000` in xcnd36

IMPORT INTO Warehouse CSV DATA ('http://xcnd36:3000/data_files/warehouse.csv') WITH nullif = 'null';
IMPORT INTO District CSV DATA ('http://xcnd36:3000/data_files/district.csv') WITH nullif = 'null';
IMPORT INTO Customer CSV DATA ('http://xcnd36:3000/data_files/customer.csv') WITH nullif = 'null';
IMPORT INTO Orders (O_W_ID, O_D_ID, O_ID, O_C_ID, O_CARRIER_ID, O_OL_CNT, O_ALL_LOCAL, O_ENTRY_D) CSV DATA ('http://xcnd36:3000/data_files/order.csv') WITH nullif = 'null';
IMPORT INTO Item CSV DATA ('http://xcnd36:3000/data_files/item.csv') WITH nullif = 'null';
IMPORT INTO OrderLine CSV DATA ('http://xcnd36:3000/data_files/order-line.csv') WITH nullif = 'null';
IMPORT INTO Stock CSV DATA ('http://xcnd36:3000/data_files/stock.csv') WITH nullif = 'null';

ALTER TABLE Orders DROP COLUMN O_CARRIER_ID; 
ALTER TABLE Carrier ADD CONSTRAINT valid_carrier CHECK (O_CARRIER_ID >= 1 AND O_CARRIER_ID <= 10);
ALTER TABLE District VALIDATE CONSTRAINT fk_d_id_ref_warehouse;
ALTER TABLE Customer VALIDATE CONSTRAINT fk_c_w_id_ref_district;
ALTER TABLE Orders VALIDATE CONSTRAINT fk_o_w_id_ref_customer;
ALTER TABLE OrderLine VALIDATE CONSTRAINT fk_ol_i_id_ref_item;
ALTER TABLE OrderLine VALIDATE CONSTRAINT fk_ol_w_id_ref_orders;
ALTER TABLE Stock VALIDATE CONSTRAINT fk_s_i_id_ref_item;
ALTER TABLE Stock VALIDATE CONSTRAINT fk_s_w_id_ref_warehouse;
