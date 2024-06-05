import psycopg2

# connect to the database

conn=psycopg2.connect(
    dbname="myduka",
    user="postgres",
    host="localhost",
    password="loise",
    port=5432
)

# initialise the cursor to perform database operation

curr=conn.cursor()


# fetch products

# def get_products():
#     query="select * from products"
#     curr.execute(query)
#     products=curr.fetchall()
#     print(products)

# get_products()    

# fetch sales

# def get_sales():
#     query='select * from sales'
#     curr.execute(query)
#     sales=curr.fetchall()
#     print(sales)

# get_sales()    


# get data- get db data of any table..... it should have a parameter open repo as mydukasystem

def get_data(table_name):
    query=f'select * from {table_name}'
    curr.execute(query)
    data=curr.fetchall()
    print(data)

# get_data('products')   


# insert data

def insert_products():
    query="insert into products(productid, name, buyingprice, sellingprice, stockquantity)\
          values (103, 'ginger', 453, 627.9, 56)"
    curr.execute(query)
    conn.commit()

# insert_products()

# get_data('products')


# create a function to insert products values as parameter (placeholder)

def insert_products(values):
    query="insert into products(productid, name ,buyingprice, sellingprice, stockquantity)values(%s ,%s, %s, %s, %s)"
    curr.execute(query,values)
    conn.commit()

# x=(104,"salt",65,80,4)
# insert_products(x)
# get_data('products')    

def insert_sales(values):
    query="insert into sales(salesid, productid, quantity, created_at)values(%s ,%s, %s, now())"
    curr.execute(query,values)
    conn.commit()

# x= (1001, 104, 35) 
# insert_sales(x)
# get_data('sales')    


# write a query that gets sales per product sales= sellingprice(in products table)*quantity(in sales table) in psql then python

# def sales_product():
#     query = "SELECT p.name, SUM(p.sellingprice * s.quantity) AS sale FROM sales s JOIN products p ON s.productid = p.productid GROUP BY p.name"
#     curr.execute(query)
#     data=curr.fetchall()
#     print(data)
   
# sales_product()


# write a query to get profit per product= (sellingprice-buyingprice)*quantity

# def profit():
#     query = "SELECT p.name, SUM((p.sellingprice - p.buyingprice) * s.quantity) AS profit FROM sales s JOIN products p ON s.productid = p.productid GROUP BY p.name"
#     curr.execute(query)
#     data=curr.fetchall()
#     print(data)
   
# profit()

# # write a query that gets sales per day sales= sellingprice(in products table)*quantity(in sales table) in psql then python hint; use the date function
# write a query to get profit per day= (sellingprice-buyingprice)*quantity

# def sales_daily():
#     query="SELECT DATE_TRUNC('day', s.created_at) AS sales_day, p.name, SUM(p.sellingprice * s.quantity) AS sales FROM sales s JOIN products p ON s.productid = p.productid GROUP BY sales_day, p.name ORDER BY sales_day"
#     curr.execute(query)
#     data=curr.fetchall()
#     print(data)
   
# sales_daily()


def profit_daily():
    query = "SELECT DATE_TRUNC('day', s.created_at) AS profit_day, p.name, SUM((p.sellingprice - p.buyingprice) * s.quantity) AS profit FROM sales s JOIN products p ON s.productid = p.productid GROUP BY profit_day, p.name ORDER BY profit_day"
    curr.execute(query)
    data=curr.fetchall()
    print(data)
   
profit_daily()