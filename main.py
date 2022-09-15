# importing the requests library
import requests

def main():
    #root node or my starting node
    starting_id = '089ef556-dfff-4ff2-9733-654645be56fe'
    #create a dictionary to save the count of each time we found a node being a child
    count_ids = {}
    #We initialize our root count in one
    count_ids[starting_id] = 1
    #we use a set for all the nodes we found so we dont have duplicates, we could calculated with the count as well
    #this slightly cleaner but more space consuming
    unique_ids = set()
    #we add our root to the set
    unique_ids.add(starting_id)
    #we use variable for the next ids we want to query, initialize with our starting node only
    nxt_ids = starting_id

    #save our url in a local variable
    URL = "https://nodes-on-nodes-challenge.herokuapp.com/nodes/"
    
    #loop while there is no more next_ids to get
    while nxt_ids != '':
        #make the get request qith out URL and ids
        r = requests.get(url = URL + nxt_ids)
        #if we dont have a success code we raise an exception
        if r.status_code != 200:
            raise Exception('Error on the request')
        #clean our next_ids
        nxt_ids = ''
        #parse response to json
        data = r.json()
        #if the json contains error throw exception
        if 'error' in data:
            raise Exception(data['error'])
        else:
            #use set variable to save our next ids to search, use set so we dont request same id twice
            tmp_ids = set()
            #loop through all the parent ids
            for d in data:
                #loop for all the child nodes of each parent id
                for i in d['child_node_ids']:
                    #add id to our tmp_ids for next ids later
                    #check if node was not already visited, avoid cycling
                    if i not in unique_ids:
                        tmp_ids.add(i)
                    #add to our set of unique ids
                    unique_ids.add(i)
                    #initialize hash in 0 if needed and increment by one
                    if i not in count_ids:
                        count_ids[i] = 0
                    count_ids[i] += 1
            #convert set to string separated by comma for next request      
            nxt_ids = ','.join(tmp_ids)

    #use hash map to calculate Which node ID is shared the most among all other nodes?
    max_shared_count = 0
    max_shared_id = ''
    for id in count_ids:
        if count_ids[id] > max_shared_count:
            max_shared_count = count_ids[id]
            max_shared_id = id
    
    print(len(unique_ids)) #amount of unique node ids
    print(max_shared_id) # Id of most shared 

main()
