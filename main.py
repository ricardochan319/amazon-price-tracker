import requests
from lxml import html
import csv
from datetime import datetime
import os

# Get URL input from the user
url = input("Enter an Amazon URL: ")

# Check if the entered URL starts with "https://www.amazon.com/"
if url.startswith("https://www.amazon.com/"):
    # Send a request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        tree = html.fromstring(response.content)

        # XPath to extract the product title
        title_xpath = '//span[@id="productTitle"]/text()'
        title = tree.xpath(title_xpath)

        # XPath to extract the product price
        price_xpath = '//span[@class="a-offscreen"]/text()'
        price = tree.xpath(price_xpath)

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print the extracted title and price
        if title:
            print("Product Title:", title[0].strip())
        else:
            print("Title not found on the page.")
            title = ['N/A']

        if price:
            current_price = float(price[0].strip().replace('$', '').replace(',', ''))
            print("Price:", current_price)
        else:
            print("Price not found on the page.")
            current_price = None

        # Check if the CSV file exists
        if os.path.exists('product_prices.csv'):
            # Read the CSV file to check for duplicate products and track the price change
            with open('product_prices.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['Product Title'].strip() == title[0].strip():
                        last_price = float(row['Price'].replace('$', '').replace(',', ''))
                        if current_price is not None and current_price < last_price:
                            print(f"Alert: The price has dropped from ${last_price} to ${current_price}!")
                        elif current_price is not None and current_price > last_price:
                            print(f"The price has increased from ${last_price} to ${current_price}.")
                        else:
                            print("The price remains unchanged.")
                        break
                else:
                    # If the loop completes without breaking, there is no duplicate product
                    # Save the information to a CSV file
                    with open('product_prices.csv', 'a', newline='') as csvfile:
                        fieldnames = ['Timestamp', 'Product Title', 'Price']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        # Write the current data
                        writer.writerow({'Timestamp': timestamp, 'Product Title': title[0].strip(), 'Price': price[0].strip() if price else 'N/A'})
        else:
            # If the CSV file doesn't exist, create it and write the header
            with open('product_prices.csv', 'w', newline='') as csvfile:
                fieldnames = ['Timestamp', 'Product Title', 'Price']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                # Write the current data
                writer.writerow({'Timestamp': timestamp, 'Product Title': title[0].strip(), 'Price': price[0].strip() if price else 'N/A'})
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
else:
    print("Please enter a valid Amazon URL.")
