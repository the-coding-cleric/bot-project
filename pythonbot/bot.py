#!/usr/bin/env python3
import argparse
import csv
import os
import sys
import time

import faker
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

CSV_FILE_NAME = "data/submission_form_database.csv"


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('run')
    args = parser.parse_args()
    return args


def generate_csv_data(output_file, fake_data_dict):
    database = pd.DataFrame(fake_data_dict)
    database.to_csv(output_file, index=False)
    database.head()


def generate_fake_data(f, message, csv_entries):
    names = [f.name() for _ in range(csv_entries)]
    first_names = []
    last_names = []
    emails = []
    messages = []
    for name in names:
        split_name = name.split(' ')
        first_names.append(split_name[0])
        last_names.append(split_name[1])
        emails.append('{}.{}@domain.com'.format(split_name[0], split_name[1]))
        messages.append(message)
    return {"first_name": first_names, "last_name": last_names, "email": emails, "message": messages}


def read_data_csv(data_file):
    """
    This reads the data from the file and if successfull returns the data.
    param input_file: str, path to the input file. Ex. data/input.csv
    return: list of data for each line of file
    """
    print('\nUsing the provided file: ' + os.path.abspath(data_file))
    try:
        with open(data_file, mode='r') as infile:
            return infile.readlines()
    except FileNotFoundError:
        sys.exit('File Not Found, {}, Exiting...\n'.format(data_file))
    except PermissionError:
        sys.exit('Permission denied - unable to read, {}. Exiting...\n'.format(data_file))
    except AttributeError:
        sys.exit('Parsing Error - {} seems to be corrupt. Exiting...\n'.format(data_file))


def make_list_from_csv(input_file_data):
    """
    This takes the data that was read from the input file and creates dict
    of each row and returns a list of these dictionaries
    return: list of dictionaries
    """
    input_list = []
    reader = csv.DictReader(input_file_data)
    for row in reader:
        input_list.append(row)
    return input_list


def answer_form_element(web_driver, element_name, value):
    form_question = web_driver.find_element(by=By.NAME, value=element_name)
    form_question.send_keys([value])
    return web_driver


def submit_form(web_driver, element_name):
    web_driver.find_element(by=By.NAME, value=element_name).click()
    return web_driver


def main():
    args = parse_args()
    f = faker.Faker()
    message = "This form is SHIT!!!!"
    if args.run:
        path = os.path.abspath(os.getcwd())
        output_file = os.path.join(path, CSV_FILE_NAME)
        csv_entries = 2
        fake_data_dict = generate_fake_data(f, message, csv_entries)
        generate_csv_data(output_file, fake_data_dict)

        element_name_dict = {"first_name": "wpforms[fields][0][first]",
                             "last_name": "wpforms[fields][0][last]",
                             "email": "wpforms[fields][1]",
                             "message": "wpforms[fields][2]"}

        csv_data = read_data_csv(output_file)
        data_list = make_list_from_csv(csv_data)

        url = "https://jeditest.wpengine.com/sample-page/"
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        for data_dict in data_list:
            driver.get(url)
            answer_form_element(driver, element_name_dict["first_name"], data_dict["first_name"])
            answer_form_element(driver, element_name_dict["last_name"], data_dict["last_name"])
            answer_form_element(driver, element_name_dict["email"], data_dict["email"])
            answer_form_element(driver, element_name_dict["message"], data_dict["message"])
            submit_form(driver, "wpforms[submit]")
            time.sleep(4)
        driver.close()


if __name__ == '__main__':
    main()
