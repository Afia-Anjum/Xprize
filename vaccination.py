# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 04:08:18 2020

@author: Asus
"""
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 15:00:46 2020

@author: Asus
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 02:19:27 2020

@author: Asus
"""

import pandas as pd

def create_adjacency_dictionary(file):
    list1 = []
    for line in file:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        list1.append(line_list)
    list1.pop(0)
    dict1={words[0]:words[1:] for words in list1}
    return list1,dict1

def create_adjacency_dictionary2(file):
    list1 = []
    for line in file:
        stripped_line = line.strip()
        #line_list = stripped_line.split()
        list1.append(stripped_line)
    list1.pop(0)
    dict1={words[0]:words[1:] for words in list1}
    return list1,dict1

def main():
    
    a_file = open("Vaccination.txt", "r") 
    country_vac=['GBR', 'USA', 'CAN', 'JPN', 'AUS', 'EU', 'RUS', 'CHN','IND','MEX']
    list1,dict1=create_adjacency_dictionary(a_file)
    #print(list1)
    #print(dict1)
    
    a_file2 = open("all_but_vac_country.txt", "r") 
    list2,dict2=create_adjacency_dictionary2(a_file2)
    
    print(list2)
    X_prize_train = pd.read_csv('Vaccine_Dec20_July21_final.csv',sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    
    date=X_prize_train['Date']
    dates=date.values.tolist()
    
    countryname=X_prize_train['CountryCode']
    country_name=countryname.values.tolist()
    
    code=X_prize_train['CountryCode']
    country_code=code.values.tolist()
    
    regionname=X_prize_train['RegionName']
    region_name=regionname.values.tolist()
    
    region=X_prize_train['RegionCode']
    region_code=region.values.tolist()
    
    juris=X_prize_train['Jurisdiction']
    jurisdiction=juris.values.tolist()
    date='20200101'
    
    D=['20201222','20210101','20210201','20210301','20210401','20210501','20210601']
    mymonth=['Dec','Jan','Feb','Mar','Apr','May','Jun']
    
    country=['GBR','USA','CAN','JPN','AUS','RUS','CHN','IND','MEX','AUT','BEL','BGR','HRV','CYP','CZE','DNK','EST','FIN','FRA','DEU','GRC','HUN','IRL','ITA','LVA','LTU','LUX','NLD','POL','PRT','ROU','SVK','SVN','ESP','SWE']
    european=['AUT','BEL','BGR','HRV','CYP','CZE','DNK','EST','FIN','FRA','DEU','GRC','HUN','IRL','ITA','LVA','LTU','LUX','NLD','POL','PRT','ROU','SVK','SVN','ESP','SWE']
    
    ###FOR VACCINATION
    
    vaccination_factor=[]
    for i in range(len(dates)):
        if i%10000==0:
            print(str(i)+" processings are done")
            
        if dates[i][4:6]=="12":
            month="Dec"
            totaldaysinmonth=31
        if dates[i][4:6]=="01":
            month="Jan"
            totaldaysinmonth=31
        if dates[i][4:6]=="02":
            month="Feb"
            totaldaysinmonth=28
        if dates[i][4:6]=="03":
            month="Mar"
            totaldaysinmonth=31
        if dates[i][4:6]=="04":
            month="Apr"
            totaldaysinmonth=30
        if dates[i][4:6]=="05":
            month="May"
            totaldaysinmonth=31
        if dates[i][4:6]=="06":
            month="Jun"
            totaldaysinmonth=30
        
        
        todaysday=int(dates[i][6:])
        try:
            index=country_vac.index(country_code[i])
            #value=(dict1[month][index]/totaldaysinmonth)*todaysday
        except:
            try:
                index=european.index(country_code[i])
                index=5
            except:
                vaccination_factor.append(1)
                continue
                
        #print(int(dict1[month][index]))
        if month=="Dec":
            v1=0
            vaccination_factor.append(1)
            continue
        elif month=="Jan":
            monthprev="Dec"
            v1=float(dict1[monthprev][index])
        elif month=="Feb":
            monthprev="Jan"
            v1=float(dict1[monthprev][index])
        elif month=="Mar":
            monthprev="Feb"
            v1=float(dict1[monthprev][index])
        elif month=="Apr":
            monthprev="Mar"
            v1=float(dict1[monthprev][index])
        elif month=="May":
            monthprev="Apr"
            v1=float(dict1[monthprev][index])
        elif month=="Jun":
            monthprev="May"
            v1=float(dict1[monthprev][index])
            
        v2=float(dict1[month][index])
        #print(v1)
        #print(v2)
        value1=(v1-v2)/totaldaysinmonth
        value2=v1-(value1*todaysday)
        #print(value2)
        vaccination_factor.append(value2)

        
     
    my_df = pd.DataFrame(vaccination_factor)
    my_df.to_csv('Vaccination_Factor.csv', index=False)    
    #TO create the vaccination dataset entries 
    
    
    
    '''
    
    print(len(list2))
    frames=[]
    #for i in range(len(country)):
    for i in range(len(list2)):
        #b=X_prize_train[X_prize_train.CountryCode==country[i]]
        b=X_prize_train[X_prize_train.CountryCode==list2[i]]
        df=b[b.Date==date]
        frames.append(df)
    result=pd.concat(frames)

    print(result)
    frames2=[]
    
    print(len(list2))
    for i in range(236):
        for j in range(len(D)):
            s=result.iloc[[i],]
            if j==0:
                n=10
            elif j==1 or j==3 or j==5:
                n=31
            elif j==2:
                n=28
            elif j==6:
                n=30
            else:
                n=30
            s=pd.concat([s]*n, ignore_index=True)
            date_integer=int(D[j])
            for m in range(n):
                type(s)
                s.iloc[m]['Date']=str(date_integer)
                date_integer+=1
            
            frames2.append(s)
    result2=pd.concat(frames2)
    
    my_df = pd.DataFrame(result2)
    my_df.to_csv('Vaccine_Dec20_July21_final.csv', index=False)
    '''
    
if __name__ == "__main__":
    main()