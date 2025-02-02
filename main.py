

import selenium
import json
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import webbrowser
from tkinter import *
import urllib
import math
from PIL import ImageTk, Image


# Array for storing Daraz product after retrieving it from Daraz website
darazProductArr = []

# Array for storing Amazon product after retrieving it from Amazon website
amazonProductArr = []

root = Tk()
root.title("Price Comparison System")
root.geometry("600x600")
search = StringVar()
state = StringVar()
state.set("Ready")

def USDtoNPR(amount):
	url = f"https://api.apilayer.com/exchangerates_data/convert?to=NPR&from=USD&amount={amount}"
	payload = {}
	headers= {
	  "apikey": "3s0PboHwgdGYDTykizxdJrH2f0osJut0"
	}
	response = requests.request("GET", url, headers=headers, data = payload)

	status_code = response.status_code
	result = response.text

	# converting string to dictionary
	r = json.loads(result)
	return f"Rs. {math.trunc(r['result'])}"

# Function to get products from Amazon
def getDetailsAmazon():
	# title = document.querySelectorAll(".s-title-instructions-style h2 a span")
	# price = .a-price .a-offscreen
	# link = .aok-relative span a
	# photo = .aok-relative span a div img
	amazonURL = f"https://www.amazon.com/s?k={search.get()}"
	# Entering options to not open the browser just get the data without opening the browser
	options = Options()
	options.headless = True
	print("Search Started")
	state.set(f"Searching {search.get()} on Amazon")

	edge_options = Options()

	# Set any desired options here, e.g., headless mode
	edge_options.use_chromium = True  # This is for the newer Chromium-based Edge

	# Create a Microsoft Edge Service instance (optional)
	edge_service = Service(r"C:\Users\Aliska\PycharmProjects\proj1\venv\test\Drivers\msedgedriver.exe")

	# Create a Microsoft Edge WebDriver instance with options
	driver = webdriver.Edge(service=edge_service, options=edge_options)
	driver.get(amazonURL)
	print("Search End")
	state.set(f"Searched Finished")

	print("Finding Elements")
	state.set(f"Finding Products....")

	# Finding Product title, price and photo
	title = driver.find_element(By.CSS_SELECTOR, ".s-title-instructions-style h2 a span")
	price = driver.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen")
	# print("price: " + str(float(price.get_attribute("textContent").replace(',', '')[1:])))

	link = driver.find_element(By.CSS_SELECTOR, f".aok-relative span a").get_attribute("href")

	photo = driver.find_element(By.CSS_SELECTOR, f".aok-relative span a div img")
	print("Elements Found")
	state.set(f"Products Found")

	print("Showing Elements on UI")
	state.set(f"Showing Products")

	# Clearing all previous items from array
	amazonProductArr.clear()

	# Adding prouduct to array
	amazonProductArr.append(link)

	amazonProductArr.append(title.text)
	nprPrice = USDtoNPR(float(price.get_attribute("textContent").replace(',', '')[1:]))
	print("npr="+ nprPrice)
	amazonProductArr.append(nprPrice)


	amazonProductArr.append(photo.get_attribute("src"))

	print("Amazon Products Done")
	state.set(f"Amazon Products Done")

	print(amazonProductArr)
	# Checking if no product found
	assert "No results found." not in driver.page_source
	driver.close()

	showAmazonProducts()


# Function to get product of name entered by the user
def getDetailsDaraz():
	productClassName = "info--ifj7U"


	darazURL = f"https://www.daraz.com.np/catalog/?q={search.get()}"
	# Entering options to not open the browser just get the data without opening the browser
	options = Options()
	options.headless = True
	print("Search Started")
	state.set(f"Searching {search.get()} on DARAZ")

	edge_options = Options()

	# Set any desired options here, e.g., headless mode
	edge_options.use_chromium = True  # This is for the newer Chromium-based Edge

	# Create a Microsoft Edge Service instance (optional)
	edge_service = Service(r"C:\Users\Aliska\PycharmProjects\proj1\venv\test\Drivers\msedgedriver.exe")

	# Create a Microsoft Edge WebDriver instance with options
	driver = webdriver.Edge(service=edge_service, options=edge_options)
	driver.get(darazURL)
	print("Search End")
	state.set(f"Searching End")
	state.set(f"Finding Products on Daraz")

	print("Finding Elements")

	# Finding Product title, price and photo
	wait = WebDriverWait(driver, 10)
	#div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f".{productClassName} .title--wFj93 a")))
	div = driver.find_element(By.CSS_SELECTOR, f".{productClassName} .title--wFj93 a")
	photo = driver.find_element(By.CSS_SELECTOR, ".img--VQr82 .mainPic--ehOdr a img")
	price = driver.find_element(By.CSS_SELECTOR, f".{productClassName} .price--NVB62 span")
	#photo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".img--VQr82 .mainPic--ehOdr a img")))
	#price= wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f".{productClassName} .price--NVB62 span")))



	link = div.get_attribute("href")
	title = div.text
	print("Elements Found")
	state.set(f"Products found on DARAZ")

	print("Showing Daraz Products")

	# Clearing all previous items from array
	darazProductArr.clear()

	# Adding prouduct to array
	darazProductArr.append(link)
	darazProductArr.append(title)
	darazProductArr.append(price.text)
	darazProductArr.append(photo.get_attribute("src"))

	print("Elements Appear on UI")
	state.set(f"Daraz Products Showed")


	# Checking if no product found
	assert "No results found." not in driver.page_source
	driver.close()

	showDarazProducts()


# Function to add spacing to text
def addSpacing(text):
	newText = ""
	i = 0
	text = text.split(" ")
	for val in text:
		if i == 10:
			newText += "\n "
			i = 0
		newText += f"{val} "
		i += 1

	return newText

def deleteFrame(frame):
	for item in frame.winfo_children():
		item.destroy()

	print("Items Deleted")


def showAmazonProducts():
	deleteFrame(amazonProductFrame)
	global amazonProductArr
	# Showing the Amazon product on UI
	darazTitle = Label(amazonProductFrame, text="AMAZON", font=("Calibri", 20, "bold"))
	darazTitle.pack()
	darazProductName = Label(amazonProductFrame, text=addSpacing(amazonProductArr[1]))
	darazProductName.pack()

	darazPriceLabel = Label(amazonProductFrame, text=amazonProductArr[2])
	darazPriceLabel.pack()

	darazLinkBtn = Button(amazonProductFrame, text="Open in AMAZON", command=lambda: webbrowser.open(amazonProductArr[0]))
	darazLinkBtn.pack()


	# Showing Amazon product photo on UI
	raw_data = urllib.request.urlopen(amazonProductArr[3])
	u = raw_data.read()
	raw_data.close()

	photo = ImageTk.PhotoImage(data=u)
	label1 = Label(amazonProductFrame, image=photo, width=600, height=600)
	label1.image = photo
	label1.pack(side=RIGHT)

	print("Amazon DONE")


def showDarazProducts():
	deleteFrame(darazProductFrame)
	global darazProductArr
	# Showing the Daraz product on UI
	darazTitle = Label(darazProductFrame, text="DARAZ", font=("Calibri", 20, "bold"))
	darazTitle.pack()
	darazProductName = Label(darazProductFrame, text=addSpacing(darazProductArr[1]))
	darazProductName.pack()

	darazPriceLabel = Label(darazProductFrame, text=darazProductArr[2])
	darazPriceLabel.pack()

	darazLinkBtn = Button(darazProductFrame, text="Open in DARAZ", command=lambda: webbrowser.open(darazProductArr[0]))
	darazLinkBtn.pack()


	# Showing Daraz product photo on UI
	raw_data = urllib.request.urlopen(darazProductArr[3])
	u = raw_data.read()
	raw_data.close()

	photo = ImageTk.PhotoImage(data=u)
	label1 = Label(darazProductFrame, image=photo, width=300, height=300)
	label1.image = photo
	label1.pack(side=RIGHT, pady=100)

	print("DONE")

def compareprice():
	pdaraz = darazProductArr[2]
	pamazon = amazonProductArr[2]
	cleaned_priceD = pdaraz.replace("Rs.", "").replace(",", "").strip()

	cleaned_priceA = pamazon.replace("Rs.", "").replace(",", "").strip()
	print(pdaraz)
	print(pamazon)
	print(cleaned_priceD)
	print(cleaned_priceA)

	if cleaned_priceD < cleaned_priceA:
		label = Label(root, text="Daraz is cheaper.", font=('Arial', 20))
		label.pack(padx=20, pady=20)
	elif cleaned_priceD > cleaned_priceA:
		label = Label(root, text="Amazon is cheaper.", font=('Arial', 20))
		label.pack(padx=20, pady=20)
	else:
		label = Label(root, text="Both have same price.", font=('Arial', 20))
		label.pack(padx=20, pady=20)

# Main function that will run when user enter product name and click on SEARCH PRODUCT
def getResult():

	getDetailsAmazon()
	getDetailsDaraz()
	compareprice()
	state.set(f"Ready")






# Search Entry for entering product name on UI
label = Label(root, text="Enter Search Result: ")
label.pack()
entry = Entry(root, textvariable=search)
entry.pack()


button = Button(root, text="Search Product", command=getResult)
button.pack()


# Product Frame for showing daraz and other websites product
productFrame = Frame(root, relief=SUNKEN)

# Daraz Frame where Daraz product will be shown
darazProductFrame = Frame(root)
darazProductFrame.pack(side=LEFT)

amazonProductFrame = Frame(root)
amazonProductFrame.pack(side=LEFT)


productFrame.pack(side=TOP, anchor=CENTER)


statusBar = Label(root, textvariable=state, relief=SUNKEN)
statusBar.pack(fill=X, side=BOTTOM)
root.mainloop()

