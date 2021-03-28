import requests
import sys
import lxml.html as lhtml
import termtables

crns = input("CRNs?: ")
crns = crns.split(",")
crns = [int(crn) for crn in crns]

term_id = 202108    # term id for Fall 2021

percent_mode = False
if len(sys.argv) > 1:
    if sys.argv[1] == '-p':
        percent_mode = True


header = ["CRN", "Class Name", "Remaining"]
table = []

for crn in crns:
    r = requests.get("https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in={}&crn_in={}".format(term_id, crn))

    if(r.status_code != 200):
        print("Error: Could not connect to oscar!")
        exit(1)


    tree = lhtml.fromstring(r.content)
    error_find = tree.xpath('//span[@class="errortext"]/text()')
    if(len(error_find) > 0):
        print("Error: Could not get information on section with CRN {}. Continuing...".format(crn))
        continue

    main_table = tree.xpath('./body/div[@class="pagebodydiv"]/table')[0]
    
    names = main_table.xpath('./tr/th/text()')[0].split(' - ')
    names = [name.strip() for name in names]
    reg_table = main_table.xpath('./tr/td/table[1]/tr[2]')[0]
    vals = reg_table.xpath('./td/text()')
    
    cap = int(vals[0])
    act = int(vals[1])
    rem = int(vals[2])

    table.append(["{}".format(names[1]), "{}".format(names[0]), "{}%".format(round(100*rem/cap, 2)) if percent_mode else "{}/{}".format(rem, cap)]) 
    
    #if percent_mode:
        #print("{} - {}\t: {}% remaining.".format(names[1], names[0], round(100*rem/cap, 2)))
    #else:
        #print("{} - {}\t: {}/{} remaining seats.".format(names[1], names[0], rem, cap))

termtables.print(table, header=header)

print("Done!")
