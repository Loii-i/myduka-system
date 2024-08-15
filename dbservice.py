from optparse import Values
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
#     return(products)

# get_products()    

# fetch sales

# def get_sales():
#     query='select * from sales'
#     curr.execute(query)
#     sales=curr.fetchall()
#     return(sales)

# get_sales()    


# get data- get db data of any table..... it should have a parameter open repo as mydukasystem

def get_data(table_name):
    query=f'select * from {table_name}'
    curr.execute(query)
    data=curr.fetchall()
    return(data)


# get_data('products')   


# insert data

def insert_products():
    query="insert into products(productid, name, buyingprice, sellingprice)\
          values (103, 'ginger', 453, 627.9)"
    curr.execute(query)
    conn.commit()

# insert_products()

# get_data('products')


# create a function to insert products values as parameter (placeholder)


def insert_products(values):
    """Insert a new product into the products table with enhanced error handling."""
    try:
        query = """
        INSERT INTO products (productid, name, buyingprice, sellingprice, bar_code) 
        VALUES (%s, %s, %s, %s, %s)
        """
        curr.execute(query, values)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()  # Rollback the transaction on error
        print(f"Error inserting product into the database: {e}")


# x=(104,"salt",65,80,4)
# insert_products(x)
# get_data('products')    

def insert_sales(values):
    """Insert a new sale into the sales table with enhanced error handling."""
    try:
        query = "INSERT INTO sales (salesid, productid, quantity, created_at) VALUES (%s, %s, %s, %s)"
        curr.execute(query, values)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()  # Rollback the transaction on error
        print(f"Error inserting sale into the database: {e}")

# x= (1001, 104, 35) 
# insert_sales(Values)
# get_data('sales')    


# write a query that gets sales per product sales= sellingprice(in products table)*quantity(in sales table) in psql then python

def sales_product():
    query = "SELECT p.name, SUM(p.sellingprice * s.quantity) AS sale FROM sales s JOIN products p ON s.productid = p.productid GROUP BY p.name"
    curr.execute(query)
    data=curr.fetchall()
    return data
   
# sales_product()


# write a query to get profit per product= (sellingprice-buyingprice)*quantity

def profit():
    query = "SELECT p.name, SUM((p.sellingprice - p.buyingprice) * s.quantity) AS profit FROM sales s JOIN products p ON s.productid = p.productid GROUP BY p.name"
    curr.execute(query)
    data=curr.fetchall()
    return(data)
   
# profit()

# # write a query that gets sales per day sales= sellingprice(in products table)*quantity(in sales table) in psql then python hint; use the date function
# write a query to get profit per day= (sellingprice-buyingprice)*quantity

def sales_daily():
    query = """
    SELECT DATE(s.created_at) AS sales_day, SUM(p.sellingprice * s.quantity) AS sales
    FROM sales s
    JOIN products p ON s.productid = p.productid
    GROUP BY sales_day
    ORDER BY sales_day
    """
    curr.execute(query)
    data = curr.fetchall()
    return data

def profit_daily():
    query = """
    SELECT DATE(s.created_at) AS profit_day, SUM((p.sellingprice - p.buyingprice) * s.quantity) AS profit
    FROM sales s
    JOIN products p ON s.productid = p.productid
    GROUP BY profit_day
    ORDER BY profit_day
    """
    curr.execute(query)
    data = curr.fetchall()
    return data

   
# profit_daily()


def recent_sales():
    query = " select * from sales order by created_at desc limit 10;"
    curr.execute(query)
    data = curr.fetchall()
    return data
# recent_sales()


def insert_user(values):
    query = "INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s);"
    curr.execute(query, values)
    conn.commit()

def check_email(email):
    query = " select * from users where email = %s;"
    curr.execute(query,(email,))
    data = curr.fetchall()
    return data

def check_email_pass(email,password):
    query = " select * from users where email = %s and password = %s;"
    curr.execute(query,(email,password,))
    data = curr.fetchall()
    return data  

    

def update_product(productid, name, buyingprice, sellingprice, bar_code):
    try:
        conn = psycopg2.connect(
            dbname="myduka",
            user="postgres",
            host="localhost",
            password="loise",
            port=5432
        )
        with conn:
            with conn.cursor() as curr:
                curr.execute("""
                    UPDATE products 
                    SET name = %s, buyingprice = %s, sellingprice = %s, bar_code = %s
                    WHERE productid = %s
                """, (name, buyingprice, sellingprice, bar_code, productid))
    except psycopg2.Error as e:
        print(f"Error updating product in the database: {e}")
        raise  # Re-raise the exception to propagate it further
    finally:
        if conn:
            conn.close()



def insert_stock(values):
    """Insert a new stock entry into the stock table with enhanced error handling."""
    try:
        query = "INSERT INTO stock (stockid, productid, quantity, created_at) VALUES (%s, %s, %s, %s)"
        curr.execute(query, values)
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()  # Rollback the transaction on error
        print(f"Error inserting stock into the database: {e}")            


def get_remaining_stock():
    query = """
    SELECT p.name, COALESCE(SUM(s.quantity), 0) - COALESCE(SUM(st.quantity), 0) AS remaining_stock
    FROM products p
    LEFT JOIN sales s ON p.productid = s.productid
    LEFT JOIN stock st ON p.productid = st.productid
    GROUP BY p.name;
    """
    curr.execute(query)
    result = curr.fetchall()
    return result

def get_remaining_stock_for_product(productid):
    query = """
    SELECT COALESCE(SUM(s.quantity), 0) - COALESCE(SUM(st.quantity), 0) AS remaining_stock
    FROM products p
    LEFT JOIN sales s ON p.productid = s.productid
    LEFT JOIN stock st ON p.productid = st.productid
    GROUP BY p.productid;
    """
    curr.execute(query, (productid,))
    result = curr.fetchone()
    return result[0] if result else 0
    
