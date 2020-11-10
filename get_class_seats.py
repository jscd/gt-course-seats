import requests
import sys

crns = input("CRNs?: ")
crns = crns.split(",")
crns = [int(crn) for crn in crns]

percent_mode = False
if len(sys.argv) > 1:
    if sys.argv[1] == '-p':
        percent_mode = True

for crn in crns:
    r = requests.get("https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=202102&crn_in={}".format(crn))
    r = r.content.decode('utf-8')

    tab_min = r.find("This table is used to present the detailed class information.")
    
    st = "<th CLASS=\"ddlabel\" scope=\"row\" >"
    sz = len(st)

    name = r[r.find(st, tab_min) + sz:r.find("<br", tab_min)]
    names = name.split(' - ')
    names = [n.strip() for n in names]


    tab_min = r.find("This layout table is used to present the seating numbers.")
    
    st = "dddefault\">"
    sz = len(st)
    cap_idx = r.find(st, tab_min) + sz
    act_idx = r.find(st, cap_idx) + sz
    rem_idx = r.find(st, act_idx) + sz
    
    cap = int(r[cap_idx:r.find("</td>", cap_idx)])
    act = int(r[act_idx:r.find("</td>", act_idx)])
    rem = int(r[rem_idx:r.find("</td>", rem_idx)])
    
    if percent_mode:
        print("{} - {}\t: {} percent remaining.".format(names[1], names[0], round(rem/cap, 2)))
    else:
        print("{} - {}\t: {}/{} remaining seats.".format(names[1], names[0], rem, cap))
    
