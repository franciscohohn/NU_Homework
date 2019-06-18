# import modules
import os
import csv
from statistics import mean

# cvs file path
csvpath = os.path.join('budget_data.csv')

# default lists
date_list = []
profit_losses = []
prof_loss_minuend = []
prof_loss_subtrahend = []
difference_list = []
date_diff_list = []
change_month_count = -1

# read csv using module
with open(csvpath, newline='') as csvfile:

    # CSV reader specifiess delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')

    # Read the header row first
    csv_header = next(csvreader) 

    # Read each row of data after the header
    for row in csvreader:
        # had to convert to int
        change_month_count = change_month_count + 1
        date_list.append(row[0])
        profit_losses.append(int(row[1]))
        prof_loss_minuend.append(int(row[1]))
        prof_loss_subtrahend.append(int(row[1]))
        
    #delete index 0
    del prof_loss_minuend[0]

    # delete last value
    del prof_loss_subtrahend[change_month_count]
    del date_list [0]

    # zip, find diffs, and add to empty list
    for a,b in zip(prof_loss_minuend, prof_loss_subtrahend):
        difference = a - b
        difference_list.append(difference)
        
    # set max and min values
    big_diff = -100000
    little_diff = 100000

    #zip, find max and min, and their associated dates
    for c,d in zip(date_list,difference_list):
        if d > big_diff:
            big_diff = d
            big_date = c
        if d < little_diff:
            little_diff = d
            little_date = c

print("Financial Analysis")
print("----------------------------")
print("Total Months: " + str(len(profit_losses)))
print("Total: $" + str(sum(profit_losses)))
print("Average Change: $" + str(round(mean(difference_list),2)))
print("Greatest Increase in Profits: " + big_date + " (" + str(big_diff) + ")")
print("Greatest Decrease in Profits: " + little_date + " (" + str(little_diff) + ")")

text_file = open("PyBank_Analysis.txt", "w")
text_file.write("Financial Analysis\n")
text_file.write("----------------------------\n")
text_file.write("Total Months: " + str(len(profit_losses)) + "\n")
text_file.write("Total: $" + str(sum(profit_losses)) + "\n")
text_file.write("Average Change: $" + str(round(mean(difference_list),2)) + "\n")
text_file.write("Greatest Increase in Profits: " + big_date + " (" + str(big_diff) + ")\n")
text_file.write("Greatest Decrease in Profits: " + little_date + " (" + str(little_diff) + ")")
text_file.close()