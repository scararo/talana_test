
def validate_number_plate(chain:str) -> bool:

    links = chain.split('-')
    
    if len(links)!=3:
        return False
    
    return links[0].isalpha() and links[1].isdigit() and links[2].isdigit()  
