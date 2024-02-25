import csv
import uuid
import smtplib
import base64

from io import BytesIO 
from sqlalchemy import func
from jinja2 import Template
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

from application.data.database import db
from application.data.models import User, Cart, CartItem, Product, Category
from flask import current_app as app
from weasyprint import HTML
import matplotlib.pyplot as plt

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "dumm@example.com"
SENDER_PASSWORD = ""

def send_email(to_address,subject, message,attachment = None):
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(message,"html"))
    print(message)
    if attachment:
        print("hii, attachment is there")
        with open(attachment,'rb') as f:
                file_data = f.read()
        file_name = attachment.split("/")[-1]
        pdf = MIMEApplication(file_data, Name=file_name)
        pdf['Content-Disposition'] = f'attachment; filename="{file_name}"'
        msg.attach(pdf)
    

    s = smtplib.SMTP(host = SMPTP_SERVER_HOST, port = SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()




def automated_mail():
    distinct_cart_ids = CartItem.query.with_entities(CartItem.cart_id).distinct().all()
    user_ids = []
    for i in distinct_cart_ids:
        user_id = Cart.query.with_entities(Cart.user_id).filter_by(cart_id = i[0]).first()
        user_ids.append(user_id[0])
    users_to_mail = []
    for i in user_ids:
        user = User.query.filter_by(id = i).first()
        users_to_mail.append(user)
    print("users to mail",users_to_mail)
    for i in users_to_mail:
        send_email(i.email, subject="Greetings user!", message = "oh no, there are still things left in your cart! Visit our app to buy them NOW !")

def send_products(email,user_id):
    csv_file_path = create_csv(user_id)
    send_email(email,subject = "Greetings manager! All products Info", message = "All products info is attached in the csv file",attachment = csv_file_path)
    print("mail sent successfully")


    

def create_csv(user_id):
    csv_file_path = 'products_details.csv'
    products = Product.query.all()
    result = []
    for product in products:
        category = Category.query.get(product.category_id)
        product_dict = {
            'id': product.id,
            'name': product.name,
            'category': category.name if category else None,
            'category_id': product.category_id,
            'price': product.price,
            'quantity': product.quantity,
            'unit': product.unit
        }
        result.append(product_dict)

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(['id', 'name','', 'category_id', 'price','quantity','unit'])   
        for product in result:
            writer.writerow([product["id"], product["name"], product["category"], product["category_id"], product["price"],product["quantity"],product["unit"]])
        
    return csv_file_path

def send_bar_plot_pdf(email,user_id):
    products = Product.query.all()
    result = []
    for product in products:
        category = Category.query.get(product.category_id)
        product_dict = {
            'id': product.id,
            'name': product.name,
            'category': category.name if category else None,
            'category_id': product.category_id,
            'price': product.price,
            'quantity': product.quantity,
            'unit': product.unit
        }
        result.append(product_dict)
    bar_plot = generate_graph_pdf(result)
    send_email(email, subject="Greetings manager! Stock available pdf", message = "All products info is attached in the pdf file",attachment = bar_plot)

def generate_graph_pdf(products):
    labels = [product['name'] for product in products]
    quantities = [product['quantity'] for product in products]
    units = [product['unit'] for product in products]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(labels, quantities)

    plt.xlabel('Product Name')
    plt.ylabel('Quantity')
    plt.title('Product Quantities Bar Plot')
    plt.xticks(rotation=45, ha='right')  

    for bar, unit in zip(bars, units):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, unit,
                ha='center', va='bottom', rotation='horizontal', fontsize=8)

    image_stream = BytesIO()
    plt.tight_layout()  
    plt.savefig(image_stream, format='png')
    plt.close()

    encoded_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    html_content = f"""
    <html>
    <body>
        <h1>Product Quantities Bar Plot</h1>
        <img src="data:image/png;base64, {encoded_image}" style="width:100%; height:auto;" >
    </body>
    </html>
    """

    pdf_file_path = 'product_quantities_plot.pdf'
    HTML(string=html_content).write_pdf(pdf_file_path)

    return pdf_file_path

