"""
Plotting Open Stocks, using Yahoo Finance Historical Data
Author: Jeffrey Yau
Date Created: 10/18/2024
Last modification: 10/19/2024
"""

import plotter
import csv
def terminate():
    userInput = input("Do you want to quit? ")

    if userInput == "Y" or userInput == "y":
        return True
    else: 
        return False    

def length(fileName, companyName): # not used, just a test
    with open("./data.csv") as inputFile:
        csvReader = csv.reader(inputFile)
        i = 0
        # this gets length vertically
        # for line in csvReader: # loops through everything horizontally
        #     print(line[1])
        #     i = i + 1
       # print(i)
        for line in csvReader: # loops through everything horizontally
            splitterLine = line[0].split(",") # splits each part of name 
            splitterLine = line[0].split(",") # splits each part of name 
            print(splitterLine[0].strip)
            i = 1
            while i < 18: # gets stuff horizontally
                print(line[i])
                i = i + 1

def plot_multiple_stocks(fileName, companyNames): # this is the main plotting function now
    with open(fileName) as inputFile:
        csvReader = csv.reader(inputFile)
        next(csvReader)
        
        plotter.init("Stock Prices", "October Business Days", "Stock Price")  # Initialize plotter 
        
        for companyName in companyNames:
            inputFile.seek(0)  # resets file pointer to the beginning for each company
            next(csvReader)  
            found = False
            
            for line in csvReader:
                splitterLine = line[0].split(",")
                if companyName == splitterLine[0].strip():
                    plotter.new_series(companyName)  # new series for each company
                    for i in range(1, 15):  # plots the stock for the company
                        plotter.add_data_point(float(line[i]))
                    found = True
                    break  # Exit loop after finding and plotting the company
            
            if not found:
                print("Company " + companyName + " not found in data.")

        plotter.plot()  # Plot all the series at once

def plot_stock(fileName, companyName): # NO LONGER IN USE, SINGLE COMPANY STOCKS
    with open(fileName) as inputFile:
        csvReader = csv.reader(inputFile) 
        next(csvReader) # skips header
        for line in csvReader: # loops through everything horizontally
            splitterLine = line[0].split(",") # splits each part  
            if companyName == splitterLine[0].strip(): # finds company
                plotter.init(companyName, "October Buisness Days", "Stock Price") # initialize the plotter
                plotter.new_series(companyName) # Each series is a new line on graph, 
                i = 1 # starts at the date where theres actually stocks
                while i < 15: 
                    plotter.add_data_point(float(line[i])) # adds each stock from each date from userInputted company
                    i = i + 1
                plotter.plot()
                return True

def company_stock(string):
    try:
        strSplit = string.split(" ")

        if strSplit[0] == "openStocks":
            companyNames = strSplit[1:] # Get all company names after the command, the [1:] gives all the elements from the second element onward
            plot_multiple_stocks(strSplit[1], companyNames)
            print("Plot finished")
        else:
            print("Plot not finished")

        '''
        THE COMMENTED OUT CODE BELOW IS ARE OUTDATED IF STATEMENTS THAT 
        THAT PREVIOUSLY USED AN OLD FUNCTION THAT COULD PLOT ONLY A SINGLE COMPANY ;-;
        '''
        # if strSplit[0] == "openStocks":
        #     stock = plot_stock(strSplit[1], strSplit[2])
        # if stock == True:
        #     print("Plot finished")
        # else:
        #     print("Plot not finished")

    except UnboundLocalError:
        print("Usage: openStocks <filename> <company1> <company2> ...")
    except FileNotFoundError:
        print("No such file: foo.csv")
    except:
        print("Unkown Error")

def help():
    print('''openStocks <filename> <company1> <company2> ... - plot each day's open stock price for specified company
            quit - quits
            help - displays this message''')

def main():
    # Tests
    '''
    openStocks ./october2024data.csv NVDA
    openStocks ./october2024data.csv AMD
    openStocks ./october2024data.csv LMT 
    '''
    boolean = False # boolean condition
    while True:
        mainInput = input(">> ")
        splitter = mainInput.split(" ") # splits message into seperate words in lists
        if splitter[0] == "help":
            help()
        if splitter[0] == "quit":
            boolean = terminate() # boolean will become either True or false
            if boolean == True:
                break
            elif boolean == False:
                boolean == False 
        company_stock(mainInput)
    #plot_stock("./data.csv", "Nvidia")
    #length("./data.csv", "Nvidia")

if __name__ == "__main__": # run guard for pytest, I don't have any rn but it's just became instinct to put it here
    main()