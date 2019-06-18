# import modules
import os
import csv
from collections import Counter
# cvs file path
csvpath = os.path.join('election_data.csv')

# default lists
total_votes = 0
recurring_candidates = []

# read csv using module
with open(csvpath, newline='') as csvfile:

    # CSV reader specifiess delimiter and variable that holds contents
    csvreader = csv.reader(csvfile, delimiter=',')

    # Read the header row first
    csv_header = next(csvreader)
    
    # Read each row of data after the header, count total_votes, create a list of candidates' names only
    for row in csvreader:
        total_votes = total_votes + 1
        recurring_candidates.append(row[2])
    
    #use imported Counter function to count instances of a value in recurring_candidates list and put results into dictionary
    candidates_votes_dict = dict(Counter(recurring_candidates))

    text_file = open("PyPoll_Analysis.txt", "w")
    print("Election Results")
    text_file.write("Election Results\n")
    print("-------------------------")
    text_file.write("-------------------------\n")
    print("Total Votes: " + str(total_votes))
    text_file.write("Total Votes: " + str(total_votes) + "\n")
    print("-------------------------")
    text_file.write("-------------------------\n")

    #loop to print keys and values in string
    #create a variable to store candidate vote percentage
    for key, value in candidates_votes_dict.items():
        candidate_percentage = (value / total_votes) * 100
        candidate_percentage_rounded = "{0:.3f}".format(candidate_percentage)
        print(str(key) + ": " + str(candidate_percentage_rounded) + "% " + "(" + str(value) + ")")
        text_file.write(str(key) + ": " + str(candidate_percentage_rounded) + "% " + "(" + str(value) + ")\n")

    print("-------------------------")
    text_file.write("-------------------------\n")

    winner_vote_count = 0

    #for each grouping of key and value, check if value is greater than zero
    #if so, that's the new count, and print name once looping is complete
    for key, value in candidates_votes_dict.items():
        if value > winner_vote_count:
            winner_vote_count = value
            winner_name = key

print("Winner: " + str(winner_name))
text_file.write("Winner: " + str(winner_name) + "\n")
print("-------------------------")
text_file.write("-------------------------\n")
text_file.close()