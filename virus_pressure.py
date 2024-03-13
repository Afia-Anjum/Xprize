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
        
    dict1={words[0]:words[1:] for words in list1}
    return list1,dict1

def population_retrieval(file):
    list1 = []
    for line in file:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        list1.append(line_list)
    
    list1.pop(0)
    us_pop_dict={words[0]:int(words[1]) for words in list1}
    return us_pop_dict

def main():
    
    #All adjacency matrix
    a_file = open("all_country_adjacency.txt", "r")  
    a_file2 = open("US_adjacency.txt", "r")  
    a_file3 = open("UK_adjacency.txt", "r")    
    
    list1,dict1=create_adjacency_dictionary(a_file)
    list2,dict2=create_adjacency_dictionary(a_file2)
    list3,dict3=create_adjacency_dictionary(a_file3)
    
    a_file.close()
    a_file2.close()
    a_file3.close()
    
    dict2={ "US_"+words[0]: words[1:] for words in list2}
    z = dict2.copy()
    z.update(dict3)
    
    

        
    X_prize_train = pd.read_csv('XPRize_naive_train.csv',sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    context_info_all_country = pd.read_csv('Additional_Context_Data_Global.csv',sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    context_info_UK = pd.read_csv('uk_populations.csv',sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    

    X_prize_train.loc[(X_prize_train.ConfirmedCases == ' '),'ConfirmedCases']=0
    X_prize_train.loc[(X_prize_train['C8_International travel controls'] == ' '),'C8_International travel controls']=0
    
    X_prize_train['ConfirmedCases'].fillna(0,inplace=True)
    X_prize_train['C8_International travel controls'].fillna(method='ffill',inplace=True)
    
    date=X_prize_train['Date']
    dates=date.values.tolist()
    
    code=X_prize_train['CountryCode']
    country_code=code.values.tolist()
    
    region=X_prize_train['RegionCode']
    region_code=region.values.tolist()
    
    juris=X_prize_train['Jurisdiction']
    jurisdiction=juris.values.tolist()
    
    C8=X_prize_train['C8_International travel controls']
    C8_controls=C8.values.tolist()
    
    case=X_prize_train['ConfirmedCases']
    cases=case.values.tolist()
    
    death=X_prize_train['ConfirmedDeaths']
    deaths=death.values.tolist()
    
 
    virus_pressure=[]
    
    #population information retrieval
    a_file4 = open("US_pop.txt", "r")    
    us_pop_dict=population_retrieval(a_file4)
    a_file4.close()
    
    pop_all_con=context_info_all_country['CountryCode']
    pop_all_country=pop_all_con.values.tolist()
    
    pop=context_info_all_country['Population']
    popu=pop.values.tolist()
    
    
    all_country_pop = {pop_all_country[i]: int(popu[i]) for i in range(len(pop_all_country))} 
    
 
    uk_pop=context_info_UK['Population']
    uk_pop_list=uk_pop.values.tolist()
    uk_pop_dict = {list3[i][0]: int(uk_pop_list[i]) for i in range(len(list3))}
    
    
    state_pop_dict = uk_pop_dict.copy()   # start with x's keys and values
    state_pop_dict.update(us_pop_dict)
    
    print(z)
    
    
    for i in range(len(dates)):
        if i%10000==0:
            print(str(i)+" processings are done")
        
        sum1=0
        sum2=0
        
        #virus pressure for region/state level entries
        if jurisdiction[i]=='STATE_TOTAL':
            pop_X=state_pop_dict[region_code[i]]
            adjacent_countries1=z[region_code[i]]
            for j in range(len(adjacent_countries1)):
                if(region_code[i].strip("_")[0:2]=="US"):
                    adjacent_countries="US_"+adjacent_countries1[j]
                    b=X_prize_train[X_prize_train.RegionCode==adjacent_countries]
                else:
                    b=X_prize_train[X_prize_train.RegionCode==adjacent_countries1[j]]
                b=b[b.Jurisdiction=='STATE_TOTAL']
                s=b[b.Date==dates[i]].ConfirmedCases
                if s.shape[0]>0:
                    confirm_y_t=int(b[b.Date==dates[i]].ConfirmedCases)
                else:
                    confirm_y_t=0
                c=b[b.Date==dates[i]]
                sum1=sum1+confirm_y_t
                if(region_code[i].strip("_")[0:2]=="US"):
                    sum2=sum2+state_pop_dict[adjacent_countries]
                else:
                    sum2=sum2+state_pop_dict[adjacent_countries1[j]]
            sum1=(pop_X*sum1)/(sum2+pop_X)    
            virus_pressure.append(float("{:.3f}".format(sum1)))
            
        #virus pressure for country level entries
        else:
            adjacent_countries=dict1[country_code[i]]
            print(adjacent_countries)
            pop_X=all_country_pop[country_code[i]]
            print(pop_X)
            for j in range(len(adjacent_countries)):
                b=X_prize_train[X_prize_train.CountryCode==adjacent_countries[j]] 
                b=b[b.Jurisdiction=='NAT_TOTAL']
                s=b[b.Date==dates[i]].ConfirmedCases
                if s.shape[0]>0:
                    confirm_y_t=int(b[b.Date==dates[i]].ConfirmedCases)
                    c=b[b.Date==dates[i]]
                    a_i_t=4-int(c['C8_International travel controls'])
                    print(confirm_y_t)
                    print(a_i_t)
                else:
                    confirm_y_t=0
                    a_i_t=0
                sum1=sum1+(confirm_y_t*a_i_t)
                sum2=sum2+all_country_pop[adjacent_countries[j]]
            print(sum1)
            print(sum2)
            sum1=(pop_X*sum1)/(sum2+pop_X)
            virus_pressure.append(float("{:.3f}".format(sum1)))
    
    print(virus_pressure)
    
    
    
    my_df = pd.DataFrame(virus_pressure)
    my_df.to_csv('virus_pressure_train.csv', index=False, header=["Virus_Pressure"])
    
    
    
    
if __name__ == "__main__":
    main()