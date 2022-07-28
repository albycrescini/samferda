import csv
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from concurrent.futures import ThreadPoolExecutor

options = webdriver.ChromeOptions()
options.headless = True

CHROME_DRIVER_PATH = "TYPE-HERE"
OUTPUT_FILE = "iceland.csv"

seats = ""
start_date = ""
end_date = ""
requesting = ""

with open(OUTPUT_FILE, "w") as f:
    wr = csv.writer(f,delimiter=";")
    wr.writerow(["requesting", "origin", "destination", "date", "time", "seats", "name", "phone", "mail", "comment"])

def rides_list():
    d = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)
    d.get("http://www.samferda.net")
    try:
        table = d.find_element(by=By.XPATH, value='//*[@id="content"]/table')
        url = table.find_elements(by=By.TAG_NAME, value='a')
        rides = list()
        for u in url:
            rides.append(u.get_attribute('href'))
    except NoSuchElementException:
        pass
    d.quit()
    return rides

def ride_details(url):
    d = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)
    d.get(url)
    try:
        table = d.find_element(by=By.XPATH, value='//*[@id="content"]/center/table')
        details = table.find_elements(by=By.TAG_NAME, value='td')
        date = details[7].text.split(".")
        details = {
            "requesting": details[1].text,
            "origin": details[3].text,
            "destination": details[5].text,
            "date": "%s-%s-%s"%(int(date[2].replace("-0", "-")), int(date[1].replace("-0", "-")), int(date[0].replace("-0", "-"))),
            "time": details[9].text,
            "seats": int(details[11].text),
            "name": details[13].text,
            "phone": details[17].text,
            "mail": details[19].text,
            "comment": details[23].text
        }

    except NoSuchElementException:
        print("Unable to get data from the website for listing: '%s'"%url)
    d.quit()
    return details

def filter_search(url):
    details = ride_details(url)
    output_list = list()
    if start_date <= details['date'] <= end_date and details['requesting'] == requesting:
        if requesting == "Passengers" and details['seats'] >= seats or requesting == "Ride" and details['seats'] <= seats:
            for key, value in details.items():
                output_list.append(value)
                print ("%s: %s"%(key, value))
            print("\n============= ---- -- ---- =============\n")

            with open(OUTPUT_FILE, "a") as f:
                wr = csv.writer(f,delimiter=";")
                wr.writerow(output_list)

def run_onthreads(url: list(), threads=7):
    with ThreadPoolExecutor(threads) as executor:
        _ = [executor.submit(filter_search, u) for u in url]
        
if __name__ == "__main__":
    while requesting not in ["Passengers", "Ride"]:
        requesting = input("Would you like to join someone else's ride [R] or to find people to join your ride? [P]: ")
        if requesting.upper() == "R":
            requesting = "Passengers" # it is the inverse because if you're looking for rides, you will only see results of people looking for passengers
        elif requesting.upper() == "P":
            requesting = "Ride" # the other way around
        else:
            print("Please type [P] if you're looking for passengers, [R] if you're looking for rides.")


    while len(start_date.split("-")) != 3:
        start_date = input("Please insert your desidered start date [yyyy-mm-dd]: ").replace("-0", "-")

    while len(end_date.split("-")) != 3:
        end_date = input("Please insert your desidered end date [yyyy-mm-dd]: ").replace("-0", "-")
        if end_date < start_date:
            print("The end date cannot be before starting date!")
            end_date = ""
    while type(seats) != int:
        try:
            seats = int(input("Please insert your desidered number of passengers: "))
        except ValueError:
            print("The number you inserted is not valid!")

    rides = rides_list()
    run_onthreads(rides, th)