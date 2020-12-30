import csv
from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Selenium Configs
options = FirefoxOptions()
options.add_argument("--headless")
driver = Firefox(options=options)

url_root = "https://www.target.com/store-locator/find-stores/"


def get_locations(zipcode):
    """
    :param zipcode: zip code to use as search parameter
    :return: list of obtained locations from zip code provided
    """
    driver.get(url_root + zipcode)
    sleep(2)
    elements = driver.find_elements_by_xpath("//span[@class='h-display-inline-block']")

    return [el.find_element_by_xpath(".//a").text for el in elements]


# Read zipcodes from file
with open("zipcodes", "r") as input_file:
    zipcodes = input_file.read().splitlines()

locations_by_zipcode = {zipcode: get_locations(zipcode) for zipcode in zipcodes}

# Save results into a csv file
try:
    with open("locations.csv", "w") as output_file:
        writer = csv.DictWriter(output_file, fieldnames="ZIP CODES; LOCATIONS")
        writer.writeheader()
        [output_file.write(f"{z}; {';'.join(ls)}\n") for z, ls in locations_by_zipcode.items()]
except IOError as ioe:
    print(f"Error: {str(ioe)}")
