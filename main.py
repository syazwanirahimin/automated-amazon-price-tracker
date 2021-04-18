import requests
import lxml
from bs4 import BeautifulSoup
import smtplib
import os

url = "https://www.amazon.co.uk/Philips-HD9721-11-Technology-Cooking-HD9721/dp/B07VXK5N9P/ref=sr_1_4?dchild=1&keywords=philips+air+fryers+for+home+use&qid=1614073436&sr=8-4"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Accept-Language": "en-US,en;q=0.5"
}

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, "lxml")
print(soup.prettify())

price = soup.find(id="priceblock_ourprice").get_text()
price_without_currency = price.split("£")[1]
price_as_float = float(price_without_currency)
print(price_as_float)

title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 100

if price_as_float < BUY_PRICE:
    message = f"{title} is now {price}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        result = connection.login(os.environ["MY_EMAIL"], os.environ["MY_PASSWORD"])
        connection.sendmail(
            from_addr=os.environ["MY_EMAIL"],
            to_addrs=os.environ["MY_EMAIL"],
            msg=f"Subject:Amazon Price Alert🚨\n\n {message}\n{url}".encode("utf8")
        )