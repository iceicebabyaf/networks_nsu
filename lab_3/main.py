from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import csv
#   fastapi
from fastapi import FastAPI, Query
from fastapi import HTTPException
from selenium import webdriver
import uvicorn
from threading import Thread
#   db
import psycopg2




DB_PARAMS = {
    "dbname": "my_parser_db",
    "user": "****",
    "password": "****",  
    "host": "localhost",
    "port": "5432"
}


def connect_to_db():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"DB connected🥶: {db_version}")
        return conn, cur
    except Exception as e:
        print(f"Beda with DB🤬: {e}")
        return None, None


def save_to_db(data, url):
    try:
        conn, cur = connect_to_db()

        if conn is None or cur is None:
            return
        
        cur.execute("TRUNCATE TABLE parsed_data RESTART IDENTITY;")
        print("DATA: \n")
        print(data)

        for i in range(len(data)):
            for j in range(len(data[i])):
                cur.execute(
                    """
                    INSERT INTO parsed_data (url, vacancy, salary, employer, location)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (url, data[i][j][0], data[i][j][1], data[i][j][2], data[i][j][3])
                )

        conn.commit()
        cur.close()
        conn.close()
        print("🤑💸📈data loaded to db🤑💸📈")

    except Exception as e:
        print(f"exception {e}")

def get_data_from_db():
    try:
        conn, cur = connect_to_db()
        if conn is None or cur is None:
            return
        
        cur.execute("SELECT * FROM parsed_data;")  
        rows = cur.fetchall()
        
        conn.close()
        
        data = [{"id": row[0], "main page link": row[1], "vacancy": row[2], "salary:": row[3], "employer": row[4], "location": row[5], } for row in rows]
        with open("/Users/xd/Desktop/comp_netw/sems/fastApi_Sql/vacancies.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("🤑💸📈data uploaded from db🤑💸📈")
        return data
    except Exception as e:
        print(f"exception get data: {e}")

def firstAttemptLogin(phone, password, driver):

    phoneNumberField = driver.find_element(By.CSS_SELECTOR, 
                                           "div.magritte-input___LVTID_7-1-8:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)")
    phoneNumberField.click()
    phoneNumberField.clear()
    phoneNumberField.send_keys(phone)

    enterWithPasswordButton = driver.find_element(By.CSS_SELECTOR, 
                                                  ".magritte-button_mode-secondary___xYz4-_5-2-18 > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
    enterWithPasswordButton.click()

    passwordField = driver.find_element(By.CSS_SELECTOR, 
                                        "div.magritte-input___LVTID_7-1-8:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)")
    passwordField.click()
    passwordField.clear()
    passwordField.send_keys(password)

    enterButton = driver.find_element(By.CSS_SELECTOR, 
                                      ".magritte-button_mode-primary___wU8PN_5-2-18 > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
    enterButton.click()


def secondAttemptLogin(phone, password, driver):
    #   logining with Big Icon "Я ищу работу"
    iSearchWorkButton = driver.find_element(By.CSS_SELECTOR, 
                                            "label.magritte-card___kxw8G_3-0-66:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
    iSearchWorkButton.click()

    enterButton = driver.find_element(By.CSS_SELECTOR, 
                                      "button.magritte-button_size-large___Gjw7e_5-2-18:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
    enterButton.click()

    phoneNumberFieldNoCountry = driver.find_element(By.XPATH, 
                                                    '/html/body/div[5]/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/form/div/div/div[3]/div[1]/div[2]/div/div/div[2]/div[1]/input')
    phoneNumberFieldNoCountry.click()
    phoneNumberFieldNoCountry.clear()
    phoneNumberFieldNoCountry.send_keys(phone)

    nextButton = driver.find_element(By.CSS_SELECTOR, 
                                     "button.magritte-button___Pubhr_5-2-18:nth-child(2) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
    nextButton.click()

    passwordField = driver.find_element(By.CSS_SELECTOR, 
                                        "div.magritte-input___LVTID_7-1-8:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)")
    passwordField.click()
    passwordField.clear()
    passwordField.send_keys(password)

    loginButton = driver.find_element(By.CSS_SELECTOR, 
                                      "button.magritte-button_size-large___Gjw7e_5-2-18:nth-child(1) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
    loginButton.click()


def thirdAttemptLogin(phone, password, driver):

    enterWithPasswordButton = driver.find_element(By.CSS_SELECTOR, 
                                                  "a.magritte-link_block___Lk0iO_5-0-2 > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
    enterWithPasswordButton.click()

    phoneNumberField = driver.find_element(By.CSS_SELECTOR, 
                                           "div.magritte-input___LVTID_7-1-8:nth-child(7) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)")
    phoneNumberField.click()
    phoneNumberField.clear()
    phoneNumberField.send_keys(phone)

    passwordField = driver.find_element(By.CSS_SELECTOR,
                                         "div.magritte-input___LVTID_7-1-8:nth-child(9) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > input:nth-child(1)")
    passwordField.click()
    passwordField.clear()
    passwordField.send_keys(password)

    loginButton = driver.find_element(By.CSS_SELECTOR, 
                                      ".magritte-button_size-large___Gjw7e_5-2-18 > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
    loginButton.click()

def loginThreeParts(phone, password, driver):
    try:
        firstAttemptLogin(phone, password, driver)
        return "Login successfully for 1 method"
    except Exception as e:
        print(f"Exception with 1 method: {e}")

    try:
        secondAttemptLogin(phone, password, driver)
        return "Login successfully for 2 method"
    except Exception as inner_e:
        print(f"Exception with 2 method: {inner_e}")

    try:
        thirdAttemptLogin(phone, password, driver)
        return "Login successfully for 3 method"
    except Exception as inner2_e:
        return(f"Exception with 2 method: {inner2_e}")
        

def parseVacancy(userVacancy):
    searchLink = 'https://novosibirsk.hh.ru/search/vacancy?text='
    for i in userVacancy:
        if i == ' ':
            i = '+'
        searchLink += i
    return searchLink

def select_filter_by_name(filter_name, driver):
    try:
        filter_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{filter_name}')]"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", filter_element)

        driver.execute_script("arguments[0].click();", filter_element)

        print(f"Filter '{filter_name}' have been marked down")

    except Exception as e:
        print(f"Couldn't found filter name '{filter_name}' \n, Exception: {e}")

def filterVacancy(vacancyFilters, driver):
    driver.find_element(By.CSS_SELECTOR, 
                                       '.supernova-wrapper--y5LhGp0Ik42f0HsU > a:nth-child(3) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1) > svg:nth-child(1)').click()
    for filter in vacancyFilters:
        select_filter_by_name(filter, driver)
    driver.find_element(By.CSS_SELECTOR,"[data-qa='advanced-search-submit-button']").click()

def onePageVacancies(driver):
    counter = 0
    vacancyFeatures = []
    for job in driver.find_elements(By.CLASS_NAME, "magritte-redesign"):
        try:

            vacancy = job.find_element(By.CSS_SELECTOR, "[data-qa='serp-item__title-text']").text
            
            try:
                salary = job.find_element(By.CSS_SELECTOR, "span[class='magritte-text___pbpft_3-0-27 magritte-text_style-primary___AQ7MW_3-0-27 magritte-text_typography-label-1-regular___pi3R-_3-0-27']").text
            except NoSuchElementException:
                salary = "Not stated"
        
            employer = job.find_element(By.CSS_SELECTOR, "[data-qa='vacancy-serp__vacancy-employer-text']").text
        
            localion = WebDriverWait(job, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-qa='vacancy-serp__vacancy-address']"))).get_attribute("textContent")
            
            if counter != 0:
                vacancyFeatures.append([vacancy, salary, employer, localion])       
                # print(vacancy, salary, employer, localion)
            counter += 1

        except NoSuchElementException:
            print("Title or price element not found.")
            continue
    return vacancyFeatures


def multiplePageParse(driver):
    outputCSV = []
    outputCSV.append(onePageVacancies(driver))


    buttons = driver.find_elements(By.CSS_SELECTOR, "a[data-qa='pager-page']")
    if buttons:
        mx = max(int(btn.text) for btn in buttons if btn.text.isdigit())

        print("MAX VALUE:", mx)


        for i in range(2, mx + 1):
            print(f"go to page: {i}")

            buttons = driver.find_elements(By.CSS_SELECTOR, "a[data-qa='pager-page']")

            for btn in buttons:
                if btn.text.isdigit() and int(btn.text) == i:
                    url = btn.get_attribute("href")
                    print("URL:", url)
                    driver.get(url)
                    outputCSV.append(onePageVacancies(driver))
                    break

    return outputCSV

    
def writeToCsv(outputArray):
    file = open("/Users/xd/Desktop/comp_netw/sems/selenium_parse/output.csv", "w")
    writer = csv.writer(file)
    writer.writerow(['vacancy', 'salary', 'employer', 'location'])

    for i in range(len(outputArray)):
        for j in range(len(outputArray[i])):
            writer.writerow(outputArray[i][j])


app = FastAPI()

def run_parser(url: str):

    driver = webdriver.Firefox()
    driver.get(url)
    
    with open('/Users/xd/Desktop/comp_netw/sems/selenium_parse/account.json', 'r') as file:
        data = json.load(file)

    userPhone = data["account"][0]["phone_number"]
    userPassword = data["account"][0]["password"]
    userVacancy = data["account"][0]["vacancy"]
    userVacancyFilter = data.get("vacancyFilter", [])



    loginThreeParts(userPhone, userPassword, driver)
    time.sleep(5)

    driver.get(parseVacancy(userVacancy))
    time.sleep(5)

    filterVacancy(userVacancyFilter, driver)
    time.sleep(5)

    output = multiplePageParse(driver)
    save_to_db(output, "https://novosibirsk.hh.ru/search/vacancy?text=python+developer")
    writeToCsv(output)

    print(f"parse URL: {url}")
    driver.quit()


@app.get("/parse")
def parse(url: str = Query(..., title="https://novosibirsk.hh.ru/")):
    thread = Thread(target=run_parser, args=(url,))
    thread.start()

@app.get("/get_data")
def get_data():
    data = get_data_from_db()
    return {"vacancies": data}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
