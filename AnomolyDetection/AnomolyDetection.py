import json
import numpy as np
import time

start = time.clock()

def add_user(userID):
    if userID not in network_data:
        network_data[userID] = {userID:0}
        
def add_acquaintance(f1,f2,degree):
    add_user(f1)
    add_user(f2)

    def add_one(acceptor,requestor):
        network_data[acceptor][requestor] = degree
    add_one(f1,f2)
    add_one(f2,f1)

def get_acq_level(f1,f2):
    try:
        return network_data[f1][f2]
    except:
        return 1000

def remove_acquaintance(f1,f2):
    add_user(f1)
    add_user(f2)
    def remove_one(acceptor,requestor):
        del network_data[acceptor][requestor]
    try:
        remove_one(f1,f2)
        remove_one(f2,f1)
    except:
        return 1

network_data = {}
purchase_data = []
flex_data = {}

def build_initial_data():
    flag = 0
    for entry in open('batch_log.json'):
        evaluated = eval(entry)
        if flag == 0:
            flex_data["D"] = evaluated["D"]
            flex_data["T"] = evaluated["T"]
            flag = 1
        elif evaluated["event_type"] == "purchase":
            purchase_data.append(evaluated)
            add_user(evaluated["id"])
        elif evaluated["event_type"] == "befriend":
            add_acquaintance(evaluated["id1"],evaluated["id2"],1)
        elif evaluated["event_type"] == "unfriend":
            remove_acquaintance(evaluated["id1"],evaluated["id2"])
    print "data initialized"
    

build_initial_data()

print len(purchase_data)

#print set(network_data["6382"])

def merge_friends(f1,f2):
    D = int(flex_data["D"])
    friendhelp = []
    first_degree = get_acq_level(f1,f2)
    if get_acq_level(f1,f2) < D:
        userFriends = set(network_data[f1])
        fFriends = set(network_data[f2])
        diff_set = fFriends - userFriends

        for acq in diff_set:
##            print get_acq_level(acq,f2) + first_degree <= D
##            print get_acq_level(acq,f2)
##            print first_degree
##            print D
            if get_acq_level(acq,f2) + first_degree <= D:
                friendhelp.append(acq)
##            print "user", userFriends
##            print "Friend", friendFriends
##            print diff_set
        for acqID in friendhelp:
            add_acquaintance(f1, acqID, get_acq_level(acqID,f2) + first_degree)
    #print "added", len(friendhelp), "to user", f1
    


def update_network(userID):
    OGuserFriends = set(network_data[userID])
    for friendID in OGuserFriends:
        merge_friends(userID,friendID)
    #print "network complete for", userID, "with", len(network_data[userID])

nets = 0        
for userID in network_data:
    if nets < 20000:
        update_network(userID)
        nets = nets + 1
        if nets % 1000 == 0:
            print nets, "networks built"
print "networks built"

int_time = time.clock()
print int_time - start
print len(purchase_data)

def get_purchase_history(userID):
    D = int(flex_data["D"])
    n = 0
    T = int(flex_data["T"])
    purchase_history = []
    for purchase in purchase_data:  
        if n == T:
            return purchase_history
        if (purchase["id"] in network_data[userID]):
            purchase_degree = network_data[userID][purchase["id"]]
            if (purchase_degree <= D):
                purchase_history.append(float(purchase["amount"]))
                n = n+1
    return purchase_history

#print get_purchase_history("6382")

email_data = []

def decide_to_email(purchase_entry):
    item_price = float(purchase_entry["amount"])
    item_history = get_purchase_history(purchase_entry["id"])
    T_mean = np.mean(item_history)
    T_SD = np.std(item_history)
    if item_price > T_mean + 3*T_SD:
        purchase_entry["mean"] = T_mean
        purchase_entry["SD"] = T_SD
        print "email", purchase_entry
        email_data.append(purchase_entry)
        return True
    else:
        return False




def process_event_data():
    for entry in open('stream_log.json'):
        evaluated = eval(entry)
        if evaluated["event_type"] == "purchase":
            add_user(evaluated["id"])
            update_network(evaluated["id"])
            decide_to_email(evaluated)
            purchase_data.insert(0,evaluated)
        elif evaluated["event_type"] == "befriend":
            f1 = evaluated["id1"]
            f2 = evaluated["id2"]
            add_acquaintance(f1,f2,1)
            merge_friends(f1,f2)
            merge_friends(f2,f1)
                              
        elif evaluated["event_type"] == "unfriend":

            remove_acquaintance(evaluated["id1"],evaluated["id2"])

process_event_data()

print len(purchase_data), "purchases"

fp_str = ""
for purchase in email_data:
    fp_str = fp_str + str(purchase) + "\n"

flagged_purchases = open("flagged_purchases.json", "w")
flagged_purchases.write(fp_str)
flagged_purchases.close()

print "purchases written"


end = time.clock()
print end - start












    


