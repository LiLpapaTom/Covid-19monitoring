#Thomas Papaloukas, ICSD14155
from urllib.parse import urlparse
import urllib.request
import csv
#Define class
class Country:
    def __init__(self, name, geo, infectedlist, infectedDate):
        self.name = name
        self.geo = geo
        self.infectedlist = infectedlist
        self.infectedDate = infectedDate
    def getobj(self):
        return self.name, self.geo, self.infectedlist, self.infectedDate
    def getname(self):
        return self.name
    def getgeo(self):
        return self.geo
    def getinfected(self):
        return self.infectedlist
    def getdate(self):
        return self.infectedDate

def menu():
    print("1.Cases in a country\n2.Cases per country\n3.Most cases\n4.Exit")

#Main
url = 'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
urlparts = urlparse(url)
if urlparts[0] == '':
    url=''.join(('http://',url))

print("Requesting confirmed COVID-19 list..")
try:
    response = urllib.request.urlopen(url)
    content = response.read()
    geturl = response.geturl()
    urlparts = urlparse(geturl)
    netloc = urlparts[1]
    if len(netloc)==0:
        fname = 'list.csv'
    else:
        fname = '.'.join((netloc,'csv'))
        print("Saving to ",fname,"..")
        fp = open(fname,'wb')
        fp.write(content)
        fp.close()
except Exception as e:
    print(e.__class__.__name__,e)

with open('raw.githubusercontent.com.csv') as csvfile:
    #read csv file
    csvreader = csv.reader(csvfile, delimiter=',')

    linecount = 0
    country = ""
    state = ""
    infection = []
    infdate = []
    date = []
    i = 0; j = 1
    obj = []
    info = []
    counter=0
    country_list = []
    total = []
    max = -1
    flag = 0
    #parse it as a list
    covidlist = list(csvreader)
    #Put the files dates in a list
    for x in range(len(covidlist[0])):
        if x > 3:
            date.append(covidlist[0][x])

    for row in covidlist:
        for x in range(len(row)):
            if x>3:
                infection.append(row[x])
                #Get the dates m/d/y
                if i+1 <= len(date):
                    infdate.append(date[i])
                    #print(infdate)
                    i += 1
            #if row is str, the 1st row is the country's states, and 2nd row the country
            if isinstance(row[0], str):
                state = row[0]
                country = row[1]
            #if 1st row is empty, means that the country has no state. therefore dont parse anything as state
            else:
                country = row[1]
        #Create the objects based on the csv information
        x = Country(country,state,list(infection),(infdate))
        obj.append(x)
        #Reset those elements, for the next iterations
        country = ""
        state = ""
        infection.clear()

for x in range(len(obj)):
    tmp = obj[x]
    tmp = tmp.getname()
    #print(tmp,'\n')

#Print all objects created based on the downloaded file
for x in range(len(obj)):
    tmp = obj[x]
    tmp = tmp.getobj()
    #print(tmp[0], tmp[1])
    infdate = tmp[2]
    infection = tmp[3]
    for y in range(len(infdate)):
        #print(infdate[y]," ",infection[y])
        break

while flag == 0:
    menu()
    x = input("Enter option: ")

    if x == '1':
        country = input("\nEnter country name: ")
        infsum = 0; infectedlist = [];

        for x in range(len(obj)):
            tmp = obj[x]
            name = tmp.getname()
            dates = tmp.getdate()
            if country.upper() == name.upper():
                #print("Exists")
                infected = tmp.getinfected()
                #print(tmp.getinfected())
                #if date matches the given date, save the date & infceted number
                for i in range(len(dates)):
                    if '/' not in infected[i]:
                        temp = int(infected[i])
                info.append(temp)

        print("Total infected people in ",country,": ",sum(info),"\n")
        info.clear()

    elif x == '2':
        date = input("\nEnter date (m/d/yy): ")
        #search for every object
        for x in range(len(obj)):
            #parse temporarelly the object, and get his information
            tmp = obj[x]
            dates = tmp.getdate()
            country = tmp.getname()
            infected = tmp.getinfected()
            state = tmp.getgeo()
            #create a list with all the countries 1 time
            if not country in country_list:
                country_list.append(country)
            #if date matches the given date, save the date & infceted number
            for i in range(len(dates)):
                if date == dates[i]:
                    temp = [country, infected[i]]
                    info.append(temp)

        case = [0 for i in range(len(country_list))]
        info.pop(0)
        #country_list.pop(0)
        #this is used in order to add the cases from same countries with different states
        #for example if we had UK xState and UKyState, sum their cases under country UK
        for i in range(len(info)):
            for j in range(len(country_list)):
                if info[i][0] == country_list[j]:
                    case[j] += int(info[i][1])

        for i in range(1,len(country_list)):
            print("\n",country_list[i]," has ", case[i], " confirmed cases.\n")
        #reset those for next iterations
        country_list.clear()
        info.clear()

    elif x == '3':
        for x in range(len(obj)):
            tmp = obj[x]
            dates = tmp.getdate()
            country = tmp.getname()
            infected = tmp.getinfected()
            state = tmp.getgeo()

            if not country in country_list:
                country_list.append(country)

            for i in range(len(dates)):
                if '/' not in infected[i]:
                    temp = [country, infected[i]]
                    info.append(temp)

        case = [0 for i in range(len(country_list))]
        info.pop(0)

        #this is used in order to add the cases from same countries with different states
        #for example if we had UK xState and UKyState, sum their cases under country UK
        for i in range(len(info)):
            for j in range(len(country_list)):
                if info[i][0] == country_list[j]:
                    case[j] += int(info[i][1])
        #Search for max value
        for i in range(len(info)):
            if int(info[i][1]) > max:
                max = int(info[i][1])
                counter = i

        print("\n",info[counter][0]," has the most cases at the moment (", info[counter][1], " confirmed cases).\n")

        country_list.clear()
        info.clear()
    elif x == '4':
        flag == 1
        break
    else:
        print("\nNot a valid option!\n")
print("Bye - bye!")
