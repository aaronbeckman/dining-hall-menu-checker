import json
import datetime
'''
with open('constants.json') as f:
    xpaths = json.load(f)

date_xpath = xpaths["date_xpath"]
months = xpaths["months"]

print(date_xpath)
print(months)
'''

today = datetime.date.today()
selected_day = datetime.date(2021, 2, 28)

print(today)
print(selected_day)
if (selected_day - today).days < 8 and (selected_day - today).days > 0:
    print("success")
print((selected_day - today).days) # yeeeee it's negative
