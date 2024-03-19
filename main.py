import time
import logging
import requests
import email_sender as email
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def findButtonAndClickByClassName(driver, className):

    # Wait for the element be loaded 
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, className))
    )  

    # Find the button by class and click
    button = driver.find_element(By.CLASS_NAME, className)
    button.click()


def findComboBoxByIDAndSelectWith(driver, id):

    # Wait for the element be loaded 
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, id))
    )  

    # Find the combo box by ID and select an option
    combo = Select(driver.find_element(By.ID, id))
    return combo


def findTextFieldAndFillWith(driver, id, value):

    # Find the text field by its ID
    text_field = driver.find_element(By.ID, id)

    # Clear any existing text in the text field
    text_field.clear()

    # Fill the text field with "bla"
    text_field.send_keys(value)


def selectComboOption(driver, id, combo, value):

    # Wait for the element be loaded 
    WebDriverWait(driver, 99999).until(
        EC.presence_of_element_located((By.ID, id))
    )  
    combo.select_by_visible_text(value)
    time.sleep(2)


def schedule(driver, name, email, residenceNumber, mobileNumber):
    # press schedule button

    # select the corret option for residence renewel
    comboIdentification = findComboBoxByIDAndSelectWith(driver, 'TipoIdentificacao')   
    selectComboOption(driver, 'TipoIdentificacao', comboIdentification, 'Residence permit')
 
    # fill the personal data
    findTextFieldAndFillWith(driver, 'NomeCliente', name)
    findTextFieldAndFillWith(driver, 'NumeroIdentificacao', residenceNumber)
    findTextFieldAndFillWith(driver, 'EmailCliente', email)
    findTextFieldAndFillWith(driver, 'TelemovelCliente', email)

    # submit the form
    print('Scheduling a appointment...')
    

def main():
    try:

        # Define the URL of the website form
        url = 'https://siga.marcacaodeatendimento.pt/Marcacao/MarcacaoInicio'
            
        # Initialize the WebDriver (make sure you have the appropriate browser driver installed)
        driver = webdriver.Chrome()  # You can also use Firefox, Safari, etc.

        # Open the webpage
        driver.get(url)
            
        # Send a GET request to fetch the form
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            
            # Parse the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')
            findButtonAndClickByClassName(driver, 'btn-entidade-assunto')
            findTextFieldAndFillWith(driver, 'tbPesquisa', 'residence permit')
            findButtonAndClickByClassName(driver, 'btn-pesquisa')
            findButtonAndClickByClassName(driver, 'btn-pesquisa-results')
            findButtonAndClickByClassName(driver, 'set-date-button')

            # Districts near Matosinhos
            myDistricts = ["AVEIRO", "COIMBRA", "PORTO", "VIANA DO CASTELO", "VILA REAL", "VISEU"]

            # Iterate over all available Districts and try an appointment in my districts
            combo_district = findComboBoxByIDAndSelectWith(driver, 'IdDistrito')   
            for district in combo_district.options:

                districtValue = district.text                
                if districtValue != 'Select a District' and districtValue in myDistricts:

                    # Select the current District 
                    logging.info(districtValue)
                    selectComboOption(driver, 'IdDistrito', combo_district, district.text)

                    # Iterate over all available Localities            
                    combo_locality = findComboBoxByIDAndSelectWith(driver, 'IdLocalidade') 
                    for locality in combo_locality.options:

                        localityValue = locality.text    
                        if localityValue != 'Select a Locality':

                            # Select the current Locality 
                            logging.info(localityValue)
                            selectComboOption(driver, 'IdLocalidade', combo_locality, locality.text)

                            # Iterate over all available Attendace Places
                            combo_place = findComboBoxByIDAndSelectWith(driver, 'IdLocalAtendimento')
                            for place in combo_place.options:

                                placeValue = place.text
                                if placeValue != 'Select an Attendance Place':
                                
                                    # Select the current Attendace Place 
                                    logging.info(placeValue)
                                    #combo_place.select_by_visible_text(place.text)
                                    selectComboOption(driver, 'IdLocalAtendimento', combo_place, place.text)

                                    # Navigate to the available places page
                                    findButtonAndClickByClassName(driver, 'set-date-button')
                                    
                                    # If has availability in this place send an email
                                    page_source = driver.page_source
                                    message = "There are no appointment shedules available for the selected criteria."
                                    #if message in page_source and 'set-appointment' not in page_source:
                                    if 'set-appointment' not in page_source:
                                        logging.info("No availability")                  
                                    else:
                                        logging.info(f"Place available!")
                                        email.send(districtValue, localityValue, placeValue)
                                        # Automatic scheduling disabled due the Captcha instaled on website
                                        #findButtonAndClickByClassName(driver, 'set-appointment')  
                                        #page_source2 = driver.page_source
                                        #print(page_source2)
                                        #schedule(driver, 'Marcio Gadelha Sampaio', 'zagadelha@gmail.com', 'K96638L13', '915000441')
                                                                                                                    
                                    driver.back() 
                                    time.sleep(2)
                                    combo_district = findComboBoxByIDAndSelectWith(driver, 'IdDistrito')    
                                    combo_locality = findComboBoxByIDAndSelectWith(driver, 'IdLocalidade') 
                                    combo_place = findComboBoxByIDAndSelectWith(driver, 'IdLocalAtendimento')
                                                                    
            logging.info("No shedules available.")
    
        else:
            logging.info("Failed to access the webpage.")

    except Exception as e:
        logging.info("APPLICATION ERROR: \n", e)

    finally:
        # Close the browser
        driver.quit()


#------------------------------- ENTRY POINT ------------------------------- 

# Aplicattion log
logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Number of times to execute main()
num_executions = 200    

# Interval between executions (in seconds)
interval = 10  

# Execute main() function X times with a X interval
for i in range(num_executions):
    logging.info('\n\nEXECUTION NUMBER: ' + str(i+1) + ' at ' + time.strftime("%H:%M:%S", time.localtime()))
    main()
    if i < num_executions - 1:
        logging.info(f"Waiting for {interval} seconds until the next execution...")
        time.sleep(interval)

