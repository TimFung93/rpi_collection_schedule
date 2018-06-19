import requests
from bs4 import BeautifulSoup as BS
import time
from lxml import etree
import datetime
import RPi.GPIO as GPIO

def get_master_schedule():
  r = requests.get("https://docs.google.com/spreadsheets/d/1Om0nwrYzeombeuMf-1pMksyG7oaTdXVpN3vR7-qrjdo/pubhtml")
  html = r.text
  bs4 = BS(html, "lxml")
  return bs4

def schedule(html):
  try:
    schedule_dict = {}
    for tr in html.find_all('tr')[2:]:
      tds = tr.find_all('td')
      schedule_dict[tds[1].text] = [tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text]
      # print "Collection Date: %s, GreenBin: %s, Garbage: %s, Recycling: %s, YardWaste: %s, ChristmasTree: %s" % \
      # (tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text, tds[6].text)
    return schedule_dict
  except:
     return "Error has occured, probably a 404, check endpoint"

def get_curret_date():
  return datetime.datetime.today().strftime('%Y/%m/%d')

def get_tomorrow_date():
  today = datetime.date.today()
  tomorrow = today + datetime.timedelta(days=1)
  return tomorrow.strftime('%Y/%m/%d')

def which_day(schedule):
  try:
    today = get_curret_date()
    light_led(schedule[today])
  except KeyError:
    tomorrow = get_tomorrow_date()
    light_led(schedule[tomorrow])
  except:
    return "Could not find schedule, can only be done day of or one day in advance"

def light_led(arr):
  if arr[1] != u'0':
    led_by(14)
  elif arr[2] != u'0':
    led_by(7)

def led_by(number):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(number, GPIO.OUT)
  GPIO.output(number, True)
  time.sleep(5)
  GPIO.output(number, False)

formatted_schedule = schedule(get_master_schedule())
which_day(formatted_schedule)