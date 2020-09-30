import requests
from tkinter import *
import json
from datetime import datetime
from urllib.request import urlopen
"""
Below are the main functions needed to connect to the api and obtain the desired data
"""

#this will connect to the api and obtain the icons corresponding to each days weather
def get_icon(api):
    i = 0
    icons = []
    while i != 8:
        icons.append(api["daily"][i]["weather"][0]["icon"])
        i+=1
    return icons

#obtain the summaries of each day from the api
def get_summarys(api):
    i = 0
    summary = []
    while i != 8:
        summary.append(api["daily"][i]["weather"][0]["description"])
        i+=1
    return summary

#get daily temps 
def get_day_temps(api):
    i = 0
    day_temps = []
    while i != 8:
        day_temps.append( str(api["daily"][i]["temp"]["day"]) + "°C")
        i+=1
    return day_temps

#obtains dates, api provides these in form of timestamps, this needs to be converted to a date
def get_dates(api):
    dates = []
    i = 0
    #as there are 8 time stamps in the api response
    while i != 8:
        timeStamp = datetime.fromtimestamp(api["daily"][i]["dt"])
        dates.append(str(timeStamp))
        i+=1
    return dates


"""
Main app window below - connects to api using user inputs for lat and lon and displays weather forecast 
in new window
"""
def find_weather(lat,lon):
    #connect to api and obtain weather info for next 8 days
    api_request = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat="+str(lat)+ "&lon=" + str(lon) +"&units=metric&exclude=current,hourly,minutely,alerts&appid=8c74f1209072a33f9839e65ba9775451")
    api = json.loads(api_request.content)
    
    #get all the weather icons,temps,summary etc for each day
    icons = get_icon(api)
    summarys = get_summarys(api)
    temps = get_day_temps(api)
    dates = get_dates(api)
    
    
    #destroy opening window and open new one
    root.destroy()
    newWindow = Tk()
    newWindow.title("Weather Summary")
    newWindow.geometry("500x650")
    
    #create canvas in which weather data will be displayed 
    cv = Canvas(newWindow,bg='dodgerblue')
    cv.pack(fill = "both",expand = True)
    
    #welcome message in window
    cv.create_text(110,25, text = "8 Day Forecast",font=('Arial',20,"bold"))
    
    #display each date
    x = 70
    y = 80
    dates1 = []
    #each date is stored in a list so that when creating text it is not overwriten by the next message
    for i, date in enumerate(dates):
        #it is date[0:10] to remove the timestamp from the string usually in yyyy/mm/dd tt:tt:tt format
        dates1.append(date[0:10])
        cv.create_text(x,y,text = dates1[i],font=('Arial',15))
        y+=75
    
    #display each icon
    x = 120
    y = 30
    pics = []
    for i, icon in enumerate(icons):
        image_url = "http://openweathermap.org/img/wn/" + str(icon) + "@2x.png"
        image_byt = urlopen(image_url).read()
        pics.append(PhotoImage(data=image_byt))
        # create_image(xpos, ypos, image, anchor)
        cv.create_image(x, y, image=pics[i], anchor='nw')
        y+=75
    
        
    #display each date
    x = 70
    y = 80
    dates1 = []
    for i, date in enumerate(dates):
        dates1.append(date[0:10])
        cv.create_text(x,y,text = dates1[i],font=('Arial',15))
        y+=75
        
   
    #display the temperatures
    temps1 = []
    x = 250
    y = 80
    for i,temp in enumerate(temps):
        temps1.append(temp)
        cv.create_text(x,y,text = temps1[i],font=('Arial',15))
        y+=75
        
        
    #display the summaries
    summarys1 = []
    x = 400
    y = 80
    for i, summary in enumerate(summarys):
        summarys1.append(summary)
        cv.create_text(x,y,text = summarys1[i],font=('Arial',15))
        y+=75
        
   
    newWindow.mainloop()

#set up opening window, user has to enter lat and lon of location to continue
root = Tk()

root.geometry("500x250")
root.title("Weather App")
root.configure(bg = "dodger blue")

welcomeLabel = Label(root,text = "Please enter a lattitude and longitude of your location :",font = ("Helvetica", 15),fg = "white",bg = "dodger blue").grid(row = 0, column = 0,columnspan = 3)

lattitude_label = Label(root,text = "Lattitude",font = ("Helvetica", 15),fg = "white",bg = "dodger blue").grid(column = 0, row = 1,pady = 20)
lattitude = Entry(root,width = 50, borderwidth = 5)
lattitude.grid(column = 1, row = 1)

longitude_label = Label(root,text = "Longitude",font = ("Helvetica", 15),fg = "white",bg = "dodger blue").grid(column = 0, row = 2,pady = 20)
longitude = Entry(root,width = 50, borderwidth = 5)
longitude.grid(column = 1, row = 2)

button = Button(root, text = "Find Forecast",width = 30,borderwidth = 5,font = ("Helvetica", 10),command = lambda : find_weather(lattitude.get(),longitude.get())).grid(column = 1, row = 3,pady = 15)

root.mainloop()


