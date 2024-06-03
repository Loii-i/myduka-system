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

def get_sales():
    query='select * from sales'
    curr.execute(query)
    sales=curr.fetchall()
    print(sales)

get_sales()    


# get data- get db data of any table..... it should have a parameter open repo as mydukasystem