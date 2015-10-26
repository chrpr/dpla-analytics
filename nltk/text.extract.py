def item_parser(item):
    "Returns raw text of selected descriptive md"

    text = ""

    for field in ["date", "description","spatial", "subject", "temporal", "title"]: 

        if field in item['sourceResource'] and item['sourceResource'][field] is not None:
            if isinstance(item['sourceResource'][field], list):
                for entry in item['sourceResource'][field]:
                    if isinstance(entry, dict):
                        if 'title' in entry.keys():
                            text += entry['title'].replace('\n','').replace('\r','') + " " 
                        elif 'displayDate' in entry.keys():
                            text +=  entry['displayDate'].replace('\n','').replace('\r','') + " "
                        elif 'name' in entry.keys():
                            text +=  entry['name'].replace('\n','').replace('\r','') + " "
                        elif 'city' in entry.keys():
                            text +=   entry['city'].replace('\n','').replace('\r','') + " "
                        elif 'state' in entry.keys():
                            text +=   entry['state'].replace('\n','').replace('\r','') + " "
                        elif 'country' in entry.keys():
                            text +=   entry['country'].replace('\n','').replace('\r','') + " "
                        elif '#text' in entry.keys():
                            text +=   entry['#text'].replace('\n','').replace('\r','') + " "
                        else:
                            text +=  str(entry).replace('\n','').replace('\r','') + " "
                    elif isinstance(entry, list):
                        text += ""
                        #weird.write(item['id'] + "|" + field + "|" + entry) + "\n")
                    elif entry is not None:
                        text += entry.replace('\n','').replace('\r','') + " "
            elif isinstance(item['sourceResource'][field], dict):
                if 'title' in item['sourceResource'][field].keys():
                    text +=  item['sourceResource'][field]['title'].replace('\n','').replace('\r','') + " "
                elif 'displayDate' in item['sourceResource'][field].keys():
                    if isinstance(item['sourceResource'][field]['displayDate'], dict):
                        text += ""
                        #weird.write(item['id'] + "|" + field + "|" + item['sourceResource'][field]['displayDate']) + "\n")
                    else: 
                        text +=  item['sourceResource'][field]['displayDate'].replace('\n','').replace('\r','') + " "
                elif 'name' in item['sourceResource'][field].keys():
                    if isinstance(item['sourceResource'][field]['name'], list):
                        text += ""
                        #weird.write(item['id'] + "|" + field + "|" + item['sourceResource'][field]['name']) + "\n")
                    else:
                        text += item['sourceResource'][field]['name'].replace('\n','').replace('\r','') + " "
                elif field == 'collection':
                    #weird.write(item['id'] + "|" + field + "|" + item['sourceResource'][field]) + "\n")
                    text += ""
                else:
                    text += item['sourceResource'][field].replace('\n','').replace('\r','') + " "
            else:  
                text += item['sourceResource'][field].replace('\n','').replace('\r','') + " "

    return(text)

