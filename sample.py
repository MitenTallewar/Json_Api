

import json
import requests
import time
class Json_Api:
    BASE_URL = 'https://jsonmock.hackerrank.com/api/football_matches'
    year = None
    drawn_matches = 0
    page = None

    def __init__(self,year):
        self.year=year

    def get_json(self):
        s = self.BASE_URL+'?year={}'.format(self.year)
        if self.page != None:
             s  = s + "&page={}".format(self.page)

        print("Calling url : ",s)
        response = requests.get(s)
        json_data = response.content
        return self.json_to_Pydata(json_data) 

    def get_total_pages(self,py_data):
        totalpages = py_data.get('total_pages')
        print('Total Pages to be checked',totalpages)
        return totalpages


    def get_api_data(self,totalpages):
        for p in range(1,totalpages+1):
            self.page = p
            print("Page no-->",p)
            py_data= self.get_json()
            matchdata = py_data.get("data")
            # print('matchdata---->',matchdata)
            for i in range(len(matchdata)):
                team1score = matchdata[i].get('team1goals')
                team2score = matchdata[i].get('team2goals')
                print("-----------------------------")
                print("team1 goals---->",team1score)
                print('team2 goals --->',team2score)
                result=self.check_draw_matches(team1score,team2score)
        return result


    def check_draw_matches(self,team1, team2):
        if team1 == team2:
            self.drawn_matches +=1
        return self.drawn_matches


    def json_to_Pydata(self,json_data):
        py_data = json.loads(json_data)
        return py_data

if __name__ == '__main__':

   print('Finding out total number of match drawn for any year:')
   y = int(input("Enter Year: "))
   start = time.time()
   j1 = Json_Api(y)

   result =j1.get_json()
   # print(result)
   pages =j1.get_total_pages(result)
   print(pages)
   total =j1.get_api_data(pages)
   print(total)
   end = time.time()
   print("time taken--",end-start)
