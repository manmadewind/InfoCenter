#-*-coding:utf-8-*-

from selenium import webdriver
import time
import datetime
import pandas as pd

dt_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

urls=[#phrase 1
      'http://hk.centadata.com/transactionhistory.aspx?type=3&code=DBPPWPPJPW',
      'http://hk.centadata.com/TransactionHistory.aspx?type=1&code=DBPPWYPXPW',
      'http://hk.centadata.com/TransactionHistory.aspx?type=1&code=DBPPWWPXPW',
      'http://hk.centadata.com/TransactionHistory.aspx?type=1&code=DBPPWPPEPW',
      # phrase 2
      'http://hk.centadata.com/TransactionHistory.aspx?type=1&code=DBPPWAPHPW',
      'http://hk.centadata.com/TransactionHistory.aspx?type=1&code=DBPPWKPHPW',
      'http://hk.centadata.com/TransactionHistory.aspx?type=1&code=DBPPWBPHPW',
      'http://hk.centadata.com/TransactionHistory.aspx?type=1&code=DBPPWGPHPW',
      # phrase 3
      'http://hk.centadata.com/TransactionHistory.aspx?type=1&code=DBPPWDPHPW',
      'http://hk.centadata.com/TransactionHistory.aspx?type=1&code=DBPPWYPHPW',
      'http://hk.centadata.com/TransactionHistory.aspx?type=1&code=DBPPWWPHPW',
      'http://hk.centadata.com/TransactionHistory.aspx?type=1&code=DBPPWWPHPW']

c_chromedriver = "./driver/mac_245_chromedriver"
driver = webdriver.Chrome(c_chromedriver)

def get_unit(j):
    l=['SA','SB','SC','SD','NA','NB','NC','ND']
    return l[j%len(l)]

# html=''
# for i, url in enumerate(urls):
#     print(i,url)
#     driver.get(url)
#     e_tables=driver.find_elements_by_class_name('unitTran-sub-table')
#     q=int(i/4) + 1
#     t=i%4 + 1
    
    
#     for j,e in enumerate(e_tables):
#         unit = get_unit(j)
#         html += "<h3>{q},{t}</h3><div>{unit}</div>\n<table>{table}</table>\n\n\n".\
#         format(table=e.get_attribute('innerHTML'), q=q, t=t,unit=unit)
#         print(q,t,unit)

# a=open('fc_raw_table.html','w')
# a.write(html)
# a.flush()
# a.close()  


df_list = []
for i, url in enumerate(urls):
    print(i,url)
    driver.get(url)
    e_tables=driver.find_elements_by_class_name('unitTran-sub-table')

    phrase = int(i/4) + 1
    tower  = i%4 + 1
    
    for j,e in enumerate(e_tables):
        unit = get_unit(j)
        html = '<table>{table}</table>'.format(table=e.get_attribute('innerHTML'))
        df_tmp_list = pd.read_html(html)
        if len(df_tmp_list)>0:
          print("ing...")
          df_tmp = df_tmp_list[0]
          df_tmp['phrase'] = phrase
          df_tmp['tower']=tower
          df_tmp['unit'] = unit
          df_list.append(df_tmp)

df_final = pd.concat(df_list)
df_final.to_csv("df_%s_FC.csv" % dt_str, sep='\t', index=False, encoding='utf-8')

print("DONE")



