def search_id(url):
    start_index = url.find('=')
    last_index = url.find('&')
    id_from_url = ''

    if last_index == -1:
        id_from_url = url[start_index + 1:]
    else:
        id_from_url = url[start_index + 1:last_index]
    
    return id_from_url