# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 02:19:27 2020

@author: Asus
"""
import osgeo.ogr
import shapely.wkt
import pandas as pd
import numpy as np

def main():
    
    '''
    shapefile = osgeo.ogr.Open("brazil_administrative.shp")
    layer = shapefile.GetLayer(0)

    countries = {} # Maps country name to Shapely geometry.

    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        country = feature.GetField("NAME")
        outline = shapely.wkt.loads(feature.GetGeometryRef().ExportToWkt())

        countries[country] = outline

    #print("Loaded %d countries" % len(countries))
    #print(countries)
    
    all_country=[]
    #other_country=[]
    
    
    print(len(countries))
    print(countries.keys())
    
    '''
    
    
    
    
    a_file = open("all_country_adjacency.txt", "r")    
    list1 = []
    for line in a_file:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        list1.append(line_list)

    a_file.close()
    
    #print(len(list1))
    #print(list1)
    dict1={words[0]:words[1:] for words in list1}
    
    a_file2 = open("US_adjacency.txt", "r")    
    list2 = []
    for line in a_file2:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        list2.append(line_list)

    a_file2.close()
    
    #print(len(list1))
    #print(list2)
    dict2={ "US_"+words[0]: words[1:] for words in list2}
    
    a_file3 = open("UK_adjacency.txt", "r")    
    list3 = []
    for line in a_file3:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        list3.append(line_list)

    a_file3.close()
    
    #print(len(list1))
    #print(list3)
    dict3={words[0]:words[1:] for words in list3}
    
    
    z = dict2.copy()   # start with x's keys and values
    z.update(dict3)
    
    a_file4 = open("US_pop.txt", "r")    
    list4 = []
    for line in a_file4:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        list4.append(line_list)

    a_file4.close()
    
    
    #print(len(list1))
    #print(list4)
    list4.pop(0)
    us_pop_dict={words[0]:int(words[1]) for words in list4}
    
    
    print(dict1)
    print(dict2)
    print(dict3)
    
    #print(us_pop_dict)
    
    
    '''
    a_file = open("US_region_names.txt", "r")

    list1 = []
    for line in a_file:
        stripped_line = line.strip()
        #line_list = stripped_line.split()
        list1.append(stripped_line)

    a_file.close()

    list1.pop(0)
    
    a_file2 = open("US_states.txt", "r")

    list2 = []
    for line in a_file2:
        stripped_line = line.strip()
        #line_list = stripped_line.split()
        list2.append(stripped_line)

    a_file2.close()

    list2.pop(0)
        
    print(list2)
	
    '''
    #for country in sorted(countries.keys()):
    #    print(country)
    
    '''
    #for country in sorted(countries.keys()):
    for country in countries.keys():
        cont=[]
        outline = countries[country]
        cont.append(country)
        #for other_country in sorted(countries.keys()):
        for other_country in countries.keys():    
            if country == other_country: 
                continue
            other_outline = countries[other_country]
            if outline.touches(other_outline):
                cont.append(other_country)
                #print("%s borders %s" % (country, other_country))
        all_country.append(cont)
    
    print(all_country)
    print(len(all_country))
    
    '''
    
    #my_df = pd.DataFrame(all_country)
    #my_df.to_csv('brazil_states_rough.csv', index=False, header=False)
    
    '''
    i=0
    for country in list1:
        cont=[]
        if country=="Kosovo":
            cont.append(list2[i])
            all_country.append(cont)
            i+=1
            continue
        #print(country)
        
        outline = countries[country]
        cont.append(list2[i])
        j=0
        for other_country in list1:
            if country == other_country or other_country=="Kosovo": 
                j+=1
                continue
            other_outline = countries[other_country]
            if outline.touches(other_outline):
                cont.append(list2[j])
            j+=1
                #print("%s borders %s" % (country, other_country))
        all_country.append(cont)
        i+=1
    
    '''
    #print(all_country)
    
    #my_df = pd.DataFrame(all_country)
    #my_df.to_csv('all_country_adjacency.csv', index=False, header=False)
    
    
    #print(len(all_country))
    
    
    #dict1={words[0]:words[1:] for words in all_country}
    #print(dict1)
    #print(dict1['SDN'])
    
    '''
    X_prize_train = pd.read_csv('XPRize_naive_test.csv',sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    #case=X_prize_train['ConfirmedCases']
    
    case_missing=X_prize_train[X_prize_train['ConfirmedCases'].isnull()]
    print(case_missing)
    #cases=case.values.tolist()
    print(case_missing.shape)
    my_df = pd.DataFrame(case_missing)
    my_df.to_csv('case_missing_Xprize_test.csv', index=False, header=False)
    '''
    
    
    
    
    X_prize_train = pd.read_csv('XPRize_naive_test.csv',sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    context_info_all_country = pd.read_csv('Additional_Context_Data_Global.csv',sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    #context_info_USA = pd.read_csv('US_states_populations.csv',sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    context_info_UK = pd.read_csv('uk_populations.csv',sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    

    #print(X_prize_train[X_prize_train['ConfirmedCases']==" "])
    X_prize_train.loc[(X_prize_train.ConfirmedCases == ' '),'ConfirmedCases']=0
    X_prize_train.loc[(X_prize_train['C8_International travel controls'] == ' '),'C8_International travel controls']=0
    #print(X_prize_train[X_prize_train['ConfirmedCases']==" "])    
    
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
    
    #print(list(X_prize_train.columns))
    virus_pressure=[]
    
    pop_all_con=context_info_all_country['CountryCode']
    pop_all_country=pop_all_con.values.tolist()
    
    pop=context_info_all_country['Population']
    popu=pop.values.tolist()
    
    
    all_country_pop = {pop_all_country[i]: int(popu[i]) for i in range(len(pop_all_country))} 
    
    #print(list3)
    uk_pop=context_info_UK['Population']
    uk_pop_list=uk_pop.values.tolist()
    uk_pop_dict = {list3[i][0]: int(uk_pop_list[i]) for i in range(len(list3))}
    
    #print(all_country_pop)
    #print(uk_pop_dict)
    
    state_pop_dict = uk_pop_dict.copy()   # start with x's keys and values
    state_pop_dict.update(us_pop_dict)
    
    print(z)
    #print(z)
    
    
    #miss=X_prize_train[X_prize_train['Date']=='20200101']['ConfirmedCases']
    #miss.fillna(0, inplace=True)
    #print(miss)
    #X_prize_train[X_prize_train['ConfirmedCases']==""]=np.NaN
    #print(X_prize_train['ConfirmedCases'].fillna(method='ffill'))
    #print(X_prize_train)
    #my_df = pd.DataFrame(X_prize_train)
    #my_df.to_csv('myDF.csv', index=False, header=False)
    
    ####FOR state/region level data
    
    '''
    for i in range(len(dates)):
        
        sum1=0
        if i>=46578 and i<=46598:
        #if i==37282:
            #x=country_code[i][3:]
            #adjacent_countries1=dict1[x]
            adjacent_countries1=dict1[country_code[i]]
            for j in range(len(adjacent_countries1)):
                #adjacent_countries="US_"+adjacent_countries1[j]
                #print(adjacent_countries)
                b=X_prize_train[X_prize_train.RegionCode==adjacent_countries1[j]]
                b=b[b.Jurisdiction=='STATE_TOTAL']
                s=b[b.Date==dates[i]].ConfirmedCases
                print(s)
                #print(b)
                if s.shape[0]>0:
                    print(i)
                    confirm_y_t=int(b[b.Date==dates[i]].ConfirmedCases)
                    c=b[b.Date==dates[i]]
                    #a_i_t=2-int(c['C7_Restrictions on internal movement'])
                    #print(int(b[b.Date==dates[i]].ConfirmedDeaths))
                    #sum1=sum1+confirm_y_t*a_i_t
                    sum1=sum1+confirm_y_t
                else:
                    sum1=sum1+0
            virus_pressure.append(sum1)
                
    my_df = pd.DataFrame(virus_pressure)
    my_df.to_csv('virus_pressure_UK_test.csv', index=False, header=False)
    
    '''
    
    
    #print(country_code)
    #print(region_code)
    
    '''
    
    ####FOR COUNTRY LEVEL DATA
    for i in range(len(dates)):
        
        #print(region_code[i])
        
        #if i <18900:
        #    continue
        if i%10000==0:
        #if i==1000:
        #    break
            print(str(i)+" processings are done")
        
        sum1=0
        if jurisdiction[i]=='STATE_TOTAL':
            #x=country_code[i][3:]
            #adjacent_countries1=dict1[x]
            #adjacent_countries1=dict1[region_code[i]]
            adjacent_countries1=z[region_code[i]]
            for j in range(len(adjacent_countries1)):
                #adjacent_countries="US_"+adjacent_countries1[j]
                #print(adjacent_countries)
                if(region_code[i].strip("_")[0:2]=="US"):
                    adjacent_countries="US_"+adjacent_countries1[j]
                    #print(adjacent_countries)
                    b=X_prize_train[X_prize_train.RegionCode==adjacent_countries]
                else:
                    b=X_prize_train[X_prize_train.RegionCode==adjacent_countries1[j]]
                b=b[b.Jurisdiction=='STATE_TOTAL']
                s=b[b.Date==dates[i]].ConfirmedCases
                #print(s)
                #print(b)
                if s.shape[0]>0:
                    #print(i)
                    confirm_y_t=int(b[b.Date==dates[i]].ConfirmedCases)
                    c=b[b.Date==dates[i]]
                    #a_i_t=2-int(c['C7_Restrictions on internal movement'])
                    #print(int(b[b.Date==dates[i]].ConfirmedDeaths))
                    #sum1=sum1+confirm_y_t*a_i_t
                    if(region_code[i].strip("_")[0:2]=="US"):
                        #adjacent_countries="US_"+adjacent_countries1[j]
                        sum1=sum1+(confirm_y_t/state_pop_dict[adjacent_countries])
                    else:
                        sum1=sum1+(confirm_y_t/state_pop_dict[adjacent_countries1[j]])
                else:
                    sum1=sum1+0
            #virus_pressure.append(sum1)
            virus_pressure.append(float("{:.3f}".format(sum1)))
        else:
            #print(country_code[i])
            adjacent_countries=dict1[country_code[i]]
            #print(adjacent_countries)
            for j in range(len(adjacent_countries)):
                b=X_prize_train[X_prize_train.CountryCode==adjacent_countries[j]] 
                b=b[b.Jurisdiction=='NAT_TOTAL']
                #print(b)
                #print(b[b.Date==dates[i]].ConfirmedCases)
                s=b[b.Date==dates[i]].ConfirmedCases
                #print(i)
                if s.shape[0]>0:
                    confirm_y_t=int(b[b.Date==dates[i]].ConfirmedCases)
                    c=b[b.Date==dates[i]]
                    #print(i)
                    #print(c['C8_International travel controls'])
                    a_i_t=4-int(c['C8_International travel controls'])
                    #print(int(b[b.Date==dates[i]].ConfirmedDeaths))
                    sum1=sum1+(confirm_y_t/all_country_pop[adjacent_countries[j]])*a_i_t
                else:
                    sum1=sum1+0
            #virus_pressure.append(sum1)
            virus_pressure.append(float("{:.3f}".format(sum1)))
    
    print(virus_pressure)
    
    
    
    my_df = pd.DataFrame(virus_pressure)
    my_df.to_csv('virus_pressure_test.csv', index=False, header=["Virus_Pressure"])
    
    
    '''
    
if __name__ == "__main__":
    main()