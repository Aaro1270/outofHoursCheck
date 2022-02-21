from datetime import datetime, time
import pandas as pd
import requests
import json
import re

def main():
    testTimes: str = ['2022-07-12T17:26:46.372Z', '2020-05-08T08:31:00.000Z', '2023-05-29T15:08:30.999Z', '2022-02-18T15:26:46.372Z', '2022-02-17T23:37:54.947Z', '2022-02-17T23:37:54.947Z', '2022-02-17T23:37:54.947Z', '2022-02-17T23:37:54.947Z', '2022-02-17T23:37:54.947Z', '2022-02-17T23:37:54.947Z', '2022-02-17T23:37:54.947Z', '2022-02-17T23:37:54.947Z']
    expectedTestResult: bool = []
    i: int = 0
    for time in testTimes:
        print('Outcome: ' + outofHoursCheck(time) + ' Expected Outcome: ' + expectedTestResult[i])
        i = i + 1
        

def outofHoursCheck(incidentTime): 
    # Function to check if the time passed as an argument is in the outofHours Defined window and if 
    # it is then the boolean True will be returned, if it is not out of hours then this function will 
    # return false
    
    # Input Format: 2022-02-17T23:26:46.372Z

    isOutofHours: bool = False


    incidentTime = re.sub('T', ' ', incidentTime) # Remove the 'T' split in the DateTime 
    incidentTime = incidentTime[:-1] # Drop the 'Z' at the end
    
    timeNow: datetime = datetime.fromisoformat(incidentTime) # Converts from the ISO formatted date into the datetime data type

    dayofWeek: int = timeNow.weekday() # Finds the day of the week as an integer
    
    if(dayofWeek >= 0 and dayofWeek <= 4 ): # If it is Monday to Friday then we enter here
        
        if((timeNow.time() >= time(17, 29)) and (timeNow.time() <= time(8,31))): # Check if the current time is inside the out of hours coverage time frame
        
            isOutofHours = True
        else: # If it is not a Weekend and is not inside coverage hours then check if it is a bank holiday
           
            bankHolidayData = requests.get(url='https://www.gov.uk/bank-holidays.json') # Pull data from the UK GOV API 
            bankHolidayDf = pd.read_json(json.dumps(bankHolidayData.json())) # Take the json data and put it inside the DataFrame

            bankHolidayDf = pd.read_json(json.dumps(bankHolidayDf.iat[1,0])) # Extracting the useful json buried inside the DataFrame 
            bankHolidayDf = bankHolidayDf['date'] # Setting the DataFrame to just be the 'data' column of the previous DataFrame
            # Strip back the DataFrame to just be the dates in England and Wales 
    

            for date in bankHolidayDf: # Check if any of the dates classed as a bank holiday match the current incident date 
                if date.date() == timeNow.date(): 
                    isOutofHours = True   
    elif(dayofWeek > 4 and dayofWeek <= 6): # If it is a Weekend day then return True
         isOutofHours = True
    else:
        # error occured log error and send notification error likely due to time format, return that it is out of hours so the incident is looked at.
        #throw the entire code in a try catch clause
        isOutofHours = True

    return isOutofHours


main()