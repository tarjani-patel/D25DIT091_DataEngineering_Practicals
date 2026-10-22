-- Create Database
CREATE DATABASE EcommerceDB;

USE EcommerceDB;

-- Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100),
    Phone VARCHAR(15),
    Address VARCHAR(255)
);

-- Products Table
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    Price DECIMAL(10,2),
    Stock INT
);

-- Orders Table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    Quantity INT,
    TotalAmount DECIMAL(10,2),
    OrderDate DATE,
    Status VARCHAR(20),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- Payments Table
CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY,
    OrderID INT,
    PaymentMethod VARCHAR(50),
    Amount DECIMAL(10,2),
    PaymentStatus VARCHAR(20),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);

-- Sample Data

INSERT INTO Customers VALUES
(101,'John Doe','john@example.com','9876543210','New York'),
(102,'Alice Smith','alice@example.com','9876543211','California');

INSERT INTO Products VALUES
(201,'Laptop','Electronics',65000,25),
(202,'Wireless Mouse','Accessories',1200,150);

INSERT INTO Orders VALUES
(301,101,201,1,65000,'2026-07-10','Delivered'),
(302,102,202,2,2400,'2026-07-11','Shipped');

INSERT INTO Payments VALUES
(401,301,'Credit Card',65000,'Success'),
(402,302,'UPI',2400,'Success');