#Version 23.08 General Utility Functions

import os
import tomli
import datetime
from xml.etree import ElementTree as xml_parser

#Open a TOML document and read its contents
def read_config(file):
    try:
        with open(file, "rb") as document:
            data = tomli.load(document)
    except (FileNotFoundError, OSError):
        data = 'ERROR: Missing Config File'
    except Exception as error:
        data = f'ERROR: Invalid Config File: {error}'
    return data

#Write log statements to a log file
def print_current_log_contents():
    date = '{:%D %I:%M%p}'.format(datetime.datetime.now())
    today  = date[:9]
    recent = datetime.datetime.strptime(date[9:],'%I:%M%p')
    recent = recent - datetime.timedelta(minutes=5)
    file = open(f'{os.getcwd()}\\log.txt', 'r', encoding = 'utf=8')
    content = file.read().split('\\n')
    for i in content:
        current_day  = (i[:9] == today)
        statement_time = datetime.datetime.strptime(i[9:16],'%I:%M%p') - datetime.timedelta(minutes=5)
        current_time = ( statement_time > recent - datetime.timedelta(minutes=5))
        if current_day and current_time:
            print(i)

#Write log statements to a log file
def log(message_type, message):
    date = '{:%D %I:%M%p}'.format(datetime.datetime.now())
    response = f'{date} {message_type}   {message}\n'
    try:
        file = open(f'{os.getcwd()}\\log.txt', 'a', encoding = 'utf=8')
    except FileNotFoundError:
        file = open(f'{os.getcwd()}\\log.txt', 'x', encoding = 'utf=8')
    file.write(response)
    file.close()
    
#Convert a string into XML
def convert_string_xml(string):
    xml = xml_parser.fromstring(string)
    return xml
    
#Convert an XML into a JSON dictionary
def convert_xml_json(xml):
    content = list(xml)
    result = {}
    #Check if any children should be in list form 
    element_names = [element.tag for element in content]
    list_names = set([item for item in element_names if element_names.count(item) > 1])
    for i in list_names:
        result[i] = []
    #Add contents
    for item in content:
        tag  = item.tag
        text = item.text
        #Add children
        children  = len(list(item))          
        if children > 0:
            node = convert_xml_json(item)
            #Add child as part of list
            if item.tag in list_names:
                result[tag].append(node)
            else:
                result[tag] = node
        else:
            result[tag] = text
    return result