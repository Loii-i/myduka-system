from flask import Flask, render_template, redirect, url_for, request, flash, session 
from datetime import datetime
from dbservice import get_data, insert_products, insert_sales, sales_product, profit, sales_daily, profit_daily, recent_sales, insert_user, check_email, check_email_pass, update_product, insert_stock,  get_remaining_stock, get_remaining_stock_for_product
  # Assuming these functions exist



# create flask instance
app = Flask(__name__)
app.secret_key = 'secret_key'


# Home route
@app.route("/")
def home():
    return render_template('home.html')

# Products route to display products and handle addition
@app.route("/products", methods=['GET', 'POST'])
def products():
     if 'email' in session:
        if request.method == 'POST':
            try:
                pid = request.form['product_id']
                pname = request.form['name']
                bprice = request.form['buyingprice']
                sprice = request.form['sellingprice']

                new_prods = (pid, pname, bprice, sprice)
                insert_products(new_prods)
                flash('Product added successfully!', 'error')

                return redirect(url_for("products"))
            except Exception as e:
                print(f"Failed to insert product: {e}")
                return render_template("products.html", prods=get_data('products'), error=str(e))

        prods = get_data('products')
        
     else:
        flash('login to view the page')
        return redirect(url_for('LogIn'))
     return render_template('products.html', prods=prods)

@app.route('/update_product', methods=['POST'])
def update_product_route():
    if request.method == 'POST':
        try:
            pid = request.form['productid']
            name = request.form['name']
            bprice = request.form['buyingprice']
            sprice = request.form['sellingprice']

            # Call update_product with individual arguments
            update_product(pid, name, bprice, sprice)

            flash('Update successful!', 'success')
        except Exception as e:
            print(f"Failed to update product: {e}")
            flash(f'Failed to update product: {e}', 'error')

    return redirect(url_for('products'))





@app.route("/sales", methods=['GET', 'POST'])
def sales():
     if 'email' in session:
            if request.method == 'POST':
                try:
                    sid = request.form['salesid']
                    pid = request.form['productid']
                    quantity = request.form['quantity']
                    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    new_sales = (sid, pid, quantity, created_at)
                    insert_sales(new_sales)
                    flash('Sale added successfully!', 'error')


                    return redirect(url_for("sales"))
                except Exception as e:
                    print(f"Failed to insert sale: {e}")
                    return render_template("sales.html", sales=get_data('sales'), prods=get_data('products'), error=str(e))

            sales = get_data('sales')
            prods = get_data('products')
     else:
        flash('login to view the page')
        return redirect(url_for('LogIn'))
     return render_template("sales.html", sales=sales, prods=prods)

@app.route("/dashboard")
def dashboard():
    if 'email' in session:
        try:
            remaining_stock = get_remaining_stock()
            labels = [row[0] for row in remaining_stock]
            values = [row[1] for row in remaining_stock]
            
            sale_p = sales_product()
            prof = profit()

            p_name = []
            p_sales = []
            prof_tot = []
            for sale in sale_p:
                p_name.append(sale[0])
                p_sales.append(float(sale[1]))
                # Find the corresponding profit for the product
                product_profit = next((x[1] for x in prof if x[0] == sale[0]), 0)
                prof_tot.append(product_profit)

            s_d = sales_daily()
            
            sales_d = []
            sales_amount = []
            for i in s_d:
                sales_d.append(str(i[0]))
                sales_amount.append(float(i[1]))

            p_d = profit_daily()
            profit_d = []
            prof_amount = []
            for i in p_d:
                profit_d.append(str(i[0]))  # Assuming i[0] is the date string
                prof_amount.append(float(i[1]))    

            r_sales = recent_sales() 
            r_sales_d = []
            for i in r_sales:
                r_sales_d.append(str(i[3]))   
                
        except Exception as e:
            flash(f"Error retrieving data: {e}", 'error')
            return redirect(url_for('LogIn'))

        return render_template("dashboard.html", 
                               p_name=p_name, p_sales=p_sales, prof_tot=prof_tot, 
                               sales_d=sales_d, sales_amount=sales_amount, 
                               profit_d=profit_d, prof_amount=prof_amount, 
                               r_sales=r_sales, labels=labels, values=values)
    else:
        flash('Login to view the page', 'error')
        return redirect(url_for('LogIn'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        f_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']

        c_email=check_email(email)
        if len(c_email) == 0:
            new_user = (f_name, email, password)

            insert_user(new_user)
            flash('registration successfully','error')
            return redirect(url_for("LogIn"))
        else:
            flash('email already exists')
       
    return render_template('register.html')


@app.route("/LogIn", methods=['GET', 'POST'])
def LogIn():
    if request.method=="POST":
        email = request.form['email']
        password = request.form['password']
        c_email=check_email(email)
        if len(c_email)==0:
            flash('register or use a different email')
        else:
            both_match=check_email_pass(email,password)
            if len(both_match)== 1:
                session['email']= email
                flash('login successfully','error')
                return redirect(url_for("dashboard"))
            else:
                flash('wrong email or password. Try again')
    return render_template('login.html')

# Logout route to handle user logout
@app.route("/logout")
def logout():
    session.pop('email', None)  # Remove the email from the session if it exists
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


# Create the Flask route for stock management
@app.route("/stock", methods=['GET', 'POST'])
def stock():
    if 'email' in session:
        if request.method == 'POST':
            try:
                sid = request.form['stockid']
                pid = request.form['productid']
                quantity = request.form['quantity']
                created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                new_stock = (sid, pid, quantity, created_at)
                insert_stock(new_stock)
                flash('Stock added successfully!', 'error')

                return redirect(url_for("stock"))
            except Exception as e:
                print(f"Failed to insert stock: {e}")
                return render_template("stock.html", stocks=get_data('stock'), prods=get_data('products'), error=str(e))

        stocks = get_data('stock')
        prods = get_data('products')
    else:
        flash('login to view the page')
        return redirect(url_for('LogIn'))
    return render_template("stock.html", stocks=stocks, prods=prods)


@app.context_processor
def inject_remaining_stock():
    def remaining_stock(productid):
        return get_remaining_stock_for_product(productid)
    return dict(remaining_stock=remaining_stock)



# Run the application
if __name__ == "__main__":
    app.run(debug=True)
