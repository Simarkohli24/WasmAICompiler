from random import random
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import pandas as pd 
import time
import random

numTrials = 10
total = 0
min = 100
max = 0
cur = 0
while (cur < numTrials):
  print(cur)
  driver = Chrome(executable_path= '/Users/simar/Desktop/GIthub-Issue-Bot/chromedriver')
  driver.get('http://localhost:8080/')
  u = random.randint(1,10)
  v = random.randint(1,10)
  try: 
    a = driver.find_element(By.XPATH, '/html/body/div/div/div[' + str(u) + ']/div[' + str(v) + ']')
    w = time.perf_counter()
    a.click()
    x = time.perf_counter()
    y = x-w
    total = total + y
    if (y < min): 
      min = y
    if (y > max): 
      max = y 
    cur = cur + 1
  except: 
    print("failed")

print(total/(numTrials))
print(min)
print(max)



# for i in range(0, 10): 
#   a = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[1]')
#   done = False 
#   while(not done): 


# driver.get('https://github.com/withfig/fig/issues/1500')
# a = driver.find_element(By.TAG_NAME, "td")
# b = driver.find_element(By.XPATH, '//*[@id="partial-discussion-header"]/div[1]/div/h1/span[1]')
# c = driver.find_element(By.XPATH, '/html/body/div[4]/div/main/turbo-frame/div/div/div/div[2]/div/div[1]/div/div[1]/div[1]/div[2]/div/div[2]/task-lists/table/tbody/tr[1]/td/details/pre');

# TRY THIS IF YOU DONT GET NONE YET then LOOP THROUGH ELEMENT
# ==============================================================================================================================
# d = driver.find_element(By.XPATH, '/html/body/div[4]/div/main/turbo-frame/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]')
# print(d.text);
# ==============================================================================================================================
# e = driver.find_element(By.XPATH, '/html/body/div[4]/div/main/turbo-frame/div/div/div/div[3]/div/div[2]/div/div[2]/div[2]')
# x = e.find_elements(By.TAG_NAME, "a"); 
# for y in x: 
#   print(y.text);
# ==============================================================================================================================
# f = driver.find_element(By.XPATH, "/html/body/div[4]/div/main/turbo-frame/div/div/div/div[1]/div[2]/div[4]/relative-time")
# print(f.get_attribute("title"))
# ==============================================================================================================================
# print(a.text);
# print(b.text);
# print(c.get_attribute("innerHTML"))



# l_output = [];
# for issue_number in range(1600, 1621):
#   driver.get('https://github.com/withfig/fig/issues/' + str(issue_number))
#   details = "No Details Found"
#   title = "No Title Found"
#   figDiagnostic = "No Fig Diagnostic Found"
#   labels = []
#   time = ""
#   try: 
#     details = driver.find_element(By.TAG_NAME, "td").text
#   except:
#     details = "No Details Found"
#   try: 
#     title = driver.find_element(By.XPATH, '//*[@id="partial-discussion-header"]/div[1]/div/h1/span[1]').text
#   except:
#     title = "No Title Found"
#   try: 
#     c = driver.find_element(By.XPATH, '/html/body/div[4]/div/main/turbo-frame/div/div/div/div[2]/div/div[1]/div/div[1]/div[1]/div[2]/div/div[2]/task-lists/table/tbody/tr[1]/td/details/pre')
#     figDiagnostic = c.text;
#   except: 
#     figDiagnostic = "No Fig Diagnostic Found"
#   try: 
#     d = driver.find_element(By.XPATH, '/html/body/div[4]/div/main/turbo-frame/div/div/div/div[2]/div/div[2]/div/div[2]/div[2]')
#     labels.append(d.text);
#   except: 
#     try:
#       e = driver.find_element(By.XPATH, '/html/body/div[4]/div/main/turbo-frame/div/div/div/div[3]/div/div[2]/div/div[2]/div[2]')
#       labels_returned = e.find_elements(By.TAG_NAME, "a"); 
#       for label in labels_returned: 
#         labels.append(label.text);
#     except:
#       labels.append("Error Getting Details");
#   try: 
#     f = driver.find_element(By.XPATH, "/html/body/div[4]/div/main/turbo-frame/div/div/div/div[1]/div[2]/div[4]/relative-time")
#     time = f.get_attribute("title")
#   except:
#     time = "Publish Date Not Found"
#   # print(issue_number);
#   # print(title);
#   # print(details);
#   # print(figDiagnostic);
#   # print(labels);
#   # print(time);
#   l = [issue_number, title, details, figDiagnostic, labels, time]
#   l_output.append(l);
#   df.append({
#     'issueNumber': issue_number,
#     'title': title,
#     'description': details,
#     'FIGDiagnostic': figDiagnostic,
#     'labels': labels,
#     'dateMade': time
#   }, ignore_index=True)

# df = pd.DataFrame(l_output, columns=['issueNumber', 'title', 'description', 'FIGDiagnostic', 'labels', 'dateMade'])
# df.to_csv("/Users/simar/Desktop/GIthub-Issue-Bot/Output2.csv")
  
