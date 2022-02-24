from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json


# This function will take an array of endpoints and will return a dictionary object with all the load timings:

def get_endpoints_call_time(driver, base_url, endpoints):
    timings = {}
    all_logs = driver.get_log('performance')
    base_url = base_url.strip('/')
    for endpoint in endpoints:
        target_url = '{}/{}'.format(base_url, endpoint)
        endpoint = endpoint.strip('/')
        url_component = '"url":"{}"'.format(target_url)
        try:
            request_sent_logs = list(
                filter(lambda x: 'Network.requestWillBeSent"' in x['message'] and url_component in x['message'],
                       all_logs))
            message_dict = json.loads(request_sent_logs[0]['message'])
            request_sent_timestamp = message_dict['message']['params']['timestamp']
            request_id = message_dict['message']['params']['requestId']
            loading_finished_logs = list(
                filter(
                    lambda x: 'Network.loadingFinished' in x['message'] and '"requestId":"{}"'.format(request_id) in x[
                        'message'], all_logs))
            message_dict = json.loads(loading_finished_logs[0]['message'])
            loading_finished_timestamp = message_dict['message']['params']['timestamp']
            time_to_load_endpoint = loading_finished_timestamp - request_sent_timestamp

        except Exception as ke:
            print(str(ke))
            time_to_load_endpoint = 'NA'
        timings[target_url] = time_to_load_endpoint
    return timings


# Turning on the chrome logging

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

driver = webdriver.Chrome(desired_capabilities=caps, executable_path='./chromedriver') # Make sure chromedriver is in PATH

driver.get('https://stackoverflow.com/')
print(get_endpoints_call_time(driver, 'https://stackoverflow.com/', ['']))

#  Output -> {'https://stackoverflow.com/': 1.3681330000981688}