#######################################################################
# Star Wars API
# Author: Saikrishna Javvadi
# Date:   13/12/2021
# Version: 1.0
# Description: A simple application that fetches data from the Star Wars API.
# References: https://swapi.dev/
#            https://www.geeksforgeeks.org/
#            https://realpython.com/python-logging/
#            https://www.nylas.com/blog/use-python-requests-module-rest-apis/
#            https://docs.python.org/3/library/urllib.error.html
#            https://docs.python.org/3/tutorial/errors.html
#            https://stackoverflow.com/questions/3420122/filter-dict-to-contain-only-certain-keys
#            https://stackoverflow.com/questions/12093773/how-to-get-json-data-from-web-page-using-python
#            https://egghead.io/lessons/python-use-a-python-generator-to-crawl-the-star-wars-api
#            https://pbpython.com/pandas-qcut-cut.html?utm_campaign=DailyPost&utm_content=103687677&utm_medium=social&utm_source=facebook&hss_channel=fbp-104940802978089
########################################################################


import json
import logging
from urllib.error import HTTPError, URLError
import pandas as pd
import requests

# Logger configuration
logging.basicConfig(level=logging.INFO)


def get_names_list(link):
    """Function to get a list of names from a link."""
    try:
        logging.info("Fetching responses from link")
        # Fetching responses from link
        response = requests.get(link)
        logging.info("Parsing JSON")
        # Parsing JSON
        api_results = json.loads(response.content)
        print(type(api_results))
        logging.info("Appending to names list")
        try:
            # for each item in the results, yield the name to the generated list
            for i in api_results['results']:
                yield i['name']
            # If there is a next page, recursively call the function
            if 'next' in api_results and api_results['next'] is not None:
                # if there is a next page, get the next page and append the names to the list
                # by recursively calling the function
                next_page = get_names_list(api_results['next'])
                for page in next_page:
                    yield page
        except Exception as e:
            print(link, "Error fetching people's names data")
    except HTTPError as e:
        print(link, "Link is not functional")
        print(e.code)
    except URLError as e:
        print(link, "Link is not functional")
        print(e.args)
    except Exception as e:
        print(link, "Invalid URL")

    """
    #Different approach to get names list
    while link:
        response = requests.get(link)
        api_results = response.json()

        for i in api_results['results']:
            # Append to names list
            yield i['name']
    
        link = api_results.get('next')
    """


def get_people_data(link):
    """Function to get people data from a link."""
    try:
        logging.info("Fetching responses from link")
        # Fetching responses from link
        response = requests.get(link)
        logging.info("Parsing JSON")
        # Parsing JSON
        api_results = json.loads(response.content)
        try:
            # for each item in the results, yield the item i to the generated list
            for i in api_results['results']:
                yield i
            # If there is a next page, recursively call the function
            if 'next' in api_results and api_results['next'] is not None:
                # if there is a next page, get the next page and append the names to the list
                # by recursively calling the function
                next_page = get_people_data(api_results['next'])
                for page in next_page:
                    yield page
        except Exception as e:
            print(link, "Error fetching people's data")
    except HTTPError as e:
        print(link, "Link is not functional")
        print(e.code)
    except URLError as e:
        print(link, "Link is not functional")
        print(e.args)
    except Exception as e:
        print(link, "Invalid URL")


def include_keys(dictionary, keys):
    """Function to filter a dict by only including certain keys."""
    try:
        # filter the dictionary to only include the wanted keys
        return {key: dictionary[key] for key in keys if key in dictionary}
    except Exception as e:
        print("Error filtering/including only required keys")


def find(arg1, arg2):
    """Function to find a value for a given key in a list."""
    people_data = get_people_data('https://swapi.dev/api/people')
    people_data = list(people_data)
    # list of wanted keys
    wanted_keys = ['name', 'height', 'mass', 'hair_color']
    logging.info("Filtering people data to contain specific keys")
    # filter people data to only include wanted keys
    filtered_list = [include_keys(person, wanted_keys) for person in people_data]
    logging.info("Finding {} in {}".format(arg2, arg1))
    print("Filtered list", filtered_list)
    # Find the given value for the given key in the filtered list
    results = [item for item in filtered_list if item[arg1] == arg2]
    return results


def profile_people(col_name, num_of_bins, is_numeric=False):
    """Function to profile people data based on the given column name."""
    people_data = get_people_data('https://swapi.dev/api/people')
    people_data = list(people_data)
    # list of wanted keys
    wanted_keys = ['name', 'height', 'mass', 'hair_color']
    logging.info("Filtering people data to contain specific keys")
    # filter people data to only include wanted keys
    filtered_list = [include_keys(person, wanted_keys) for person in people_data]
    logging.info("Profiling {}".format(col_name))
    # Profile the given column name
    df = pd.DataFrame(filtered_list)
    # replace '-', 'None','unknown' with None
    df.replace({'-': None, 'None': None, 'unknown': None}, inplace=True)
    # if the column is numeric, bin the data
    if is_numeric:
        # remove ',' and cast as float
        df[col_name] = df[col_name].str.replace(',', '').astype(float)
        # create a histogram of the column
        return pd.qcut(df[col_name], num_of_bins).value_counts()
    else:
        # for a categorical column create a count of the column for each value
        return df[col_name].value_counts()


if __name__ == "__main__":
    """Main function."""

    people_names_data = get_names_list('https://swapi.dev/api/')
    people_names_data = list(people_names_data)

    print(people_names_data)
    print(len(people_names_data))

    people_data = get_people_data('https://swapi.dev/api/people')
    people_data = list(people_data)

    print(type(people_data))
    print(len(people_data))

    find_res = find('name', 'Darth Vader')
    print(find_res)
    print(len(find_res))
    print(find_res[0]['height'])

    res = profile_people('height', 5, is_numeric=True)
    print(res)
    print(type(res))
