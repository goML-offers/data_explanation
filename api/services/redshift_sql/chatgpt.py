import os
import openai
import logging
import json

class ChatGPT:

    # Modified startMessageStack with the provided table metadata
    startMessageStack = [
    {"role": "system", "content": "You act as the middleman between USER and a DATABASE. Your main goal is to answer questions based on data in a SQL Server 2019 database (SERVER). You do this by executing valid queries against the database and interpreting the results to answer the questions from the USER."},
    {"role": "user", "content": "From now you will only ever respond with JSON. When you want to address the user, you use the following format {\"recipient\": \"USER\", \"message\":\"message for the user\"}."},
    {"role": "assistant", "content": "{\"recipient\": \"USER\", \"message\":\"I understand.\"}."},
    {"role": "user", "content": "You can address the SQL Server by using the SERVER recipient. When calling the server, you must also specify an action. The action can be QUERY when you want to QUERY the database, or SCHEMA when you need SCHEMA information for a comma-separated list of tables. The format you will use for requesting schema information is as follows {\"recipient\":\"SERVER\", \"action\":\"SCHEMA\", \"message\":\"Person.Person, Person.Address\"}. The format you will use for executing a query is as follows: {\"recipient\":\"SERVER\", \"action\":\"QUERY\", \"message\":\"SELECT SUM(OrderQty) FROM Sales.SalesOrderDetail;\"}"},
    {"role": "user", "content": "The following tables are available in the database: zipcode, voucher, supplier, reviews, product, product_group, product_details, payment, orders, order_product, employee, employee_new, customer, customer_fix, bill, order_table, address."},
    {"role": "user", "content": "Table, Column, DataType\nzipcode, city, character varying\nzipcode, state, character varying\nzipcode, zipcode_id, bigint\norders, payment_id, character varying\norders, shippent_duration, character varying\norders, status, character varying\norders, order_date, character varying\norders, order_id, character varying"},
    {"role": "user", "content":"""zipcode Table - Zip Code Information

Columns: city (text), state (text), zipcode_id (unique identifier as a number).
voucher Table - Voucher Details

Columns: voucher_id (unique identifier as text), discount% (discount percentage as a number).
supplier Table - Supplier Information

Columns: supplier_name (text), supplier_id (unique identifier as text), supply_quantity (quantity supplied as a number).
reviews Table - Product Reviews

Columns: product_id (unique identifier as text), review_id (unique identifier as text), defect% (defect percentage as a number), quality_rating (quality rating as a number).
product Table - Product Details

Columns: supplier_id (unique identifier as text), product_name (text), product_id (unique identifier as text), group_id (unique identifier as a number), available_number (available quantity as a number).
product_group Table - Product Group Information

Columns: group_name (text), group_id (unique identifier as a number).
product_details Table - Product Details

Columns: colour (text), product_id (unique identifier as text), height (height as a decimal number), width (width as a decimal number), weight (weight as a number).
payment Table - Payment Details

Columns: name_on_card (text), card_type (text), payment_mode (text), payment_id (unique identifier as text), visit_number (visit number as a number), customer_id (customer identifier as a number), cvv (CVV as a number), card_number (card number as a number).
orders Table - Order Information

Columns: payment_id (unique identifier as text), shippent_duration (shipping duration as text), status (order status as text), order_date (order date as text), order_id (unique identifier as text).
order_product Table - Order Product Details

Columns: orderproduct_id (unique identifier as text), order_id (unique identifier as text), product_id (unique identifier as text), quantity (quantity ordered as a number).
employee Table - Employee Information

Columns: employee_type (text), employee_name (text), employee_id (unique identifier as text), join_date (text), department (text), designation (text), salary (salary as a number), ssn (Social Security Number as a number).
employee_new Table - New Employee Information

Columns: employee_id (unique identifier as text), name_on_card (text), card_type (text), payment_mode (text), payment_id (unique identifier as text), visit_number (visit number as a number), customer_id (customer identifier as a number), cvv (CVV as a number), card_number (card number as a number).
customer Table - Customer Information

Columns: customer_type (text), email_address (text), last_name (text), first_name (text), phone_number (phone number as a number), customer_id (unique identifier as a number).
customer_fix Table - Fixed Customer Information

Columns: employee_id (text), customer_type (text), email_address (text), last_name (text), first_name (text), phone_number (phone number as a number), customer_id (unique identifier as a number).
bill Table - Billing Information

Columns: order_id (unique identifier as text), payment_id (unique identifier as text), voucher_id (unique identifier as text), billing_id (unique identifier as text), amount_paid (amount paid as a number).
order_table Table - Order Information

Columns: payment_id (unique identifier as text), shippent_duration (shipping duration as text), status (order status as text), order_date (order date as text), order_id (unique identifier as text).
address Table - Address Information

Columns: apartment_name (text), street (text), address_id (unique identifier as text), unnamed: 6 (double precision), unnamed: 5 (double precision), customer_id (customer identifier as a number), apartment_number (apartment number as a number)."""}  ,
    {"role": "user", "content": "You should create quires based on the question i am asking, to retrieve it from the database, if required make join queries also"}  
       ]


    def __init__(self, api_key, api_org = "", model = "gpt-3.5-turbo"):
        if api_org:
            openai.api_key
        openai.api_key = api_key
        self.model = model
        self.messages = self.startMessageStack.copy()

    def message(self, message, sender):
        logging.debug(message)
        if (sender):
            message = json.dumps({'message':message, 'sender':sender})
        self.messages.append({"role": "user", "content": message})
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        response = completion.choices[0].message.content 
        logging.debug(response)
        self.messages.append({"role": "assistant", "content": response})
        return response

    def reset(self):
        self.messages = self.startMessageStack.copy()
        print('model was reset to intial state')

