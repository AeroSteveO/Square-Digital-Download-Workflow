

from square.client import Client
import json
import smtplib

application_secret = 'SQUARE-API-SECRET'
gmail_user='my-craft-email@gmail.com'
gmail_password='MY_STRONG_PASSWORD'
storeItemNames = ['cool quilt pattern', 'cool quilt kit']
digitalItemName = 'Cool Quilt Pattern'
sent_from = 'my-craft-email@gmail.com'
downloadLink = 'https://my.file.source.com/myfile'
body = 'Thank you for purchasing the ' + digitalItemName + '! Below is the link where you can download your digital copy. '\
    + 'This link will be active for two weeks; please be sure to download your pattern within that time period. '\
    + 'If you have any questions or need any assistance, please feel free to contact me by emailing me directly at '\
    + 'my-craft-email@gmail.com or by reaching out through the contact form on the website.'\
    + '\n\nDownload Link: ' + downloadLink +\
    '\n\nThank you again for your support!\nMy Crafts\n@IG\nhttps://my-site.square.site'
subject = digitalItemName + ' Download Link'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, sent_from, subject, body)

client = Client(
    access_token=application_secret,
    environment='production'
)

result = client.orders.search_orders(
  body = {
    "location_ids": [
      "SQUARE-LOCATION-ID"
    ],
    "query": {
      "filter": {
        "state_filter": {
          "states": [
            "OPEN"
          ]
        },
        "fulfillment_filter": {
          "fulfillment_types": [
            "DIGITAL"
          ]
        }
      }
    }
  }
)

if result.is_error():
  print(result.errors)
  exit(-1)

if not bool(result.body):
    print('No orders to process. Exiting...')
    exit(0)

emailAddresses = []
orderIds = []
orderVersion = []
orderFulfilmentUIDs = []

#for each order in body
for order in result.body['orders']:
    lineItems = order['line_items']
    hasItem = False
    for item in lineItems:
        if item['name'].lower() in storeItemNames:
            hasItem = True
            break
    if not hasItem: continue
    localCustomer = client.customers.retrieve_customer(
        customer_id = order['customer_id']
    )
    emailAddresses.append(localCustomer.body['customer']['email_address'])
    orderIds.append(order['id'])
    orderVersion.append(order['version'])
    orderFulfilmentUIDs.append(order['fulfillments'][0]['uid'])

if len(emailAddresses) == 0:
    print('No emails to distribute downloads to. Exiting...')
    exit(0)

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, emailAddresses, email_text)
    server.close()
except:
    print('Something went wrong...')
    exit(-1)


for i in range(len(orderIds)):
    fulfilmentResult = client.orders.update_order(
        order_id = orderIds[i],
        body = {
            "order": {
                "location_id": "SQUARE_LOCATION_ID",
                "fulfillments": [
                    {
                        "state": "COMPLETED",
                        'uid': orderFulfilmentUIDs[i]
                    }
                ],
                "state": "COMPLETED",
                "version": orderVersion[i]
            }
        }
    )
    if fulfilmentResult.is_error():
        print(result.errors)

