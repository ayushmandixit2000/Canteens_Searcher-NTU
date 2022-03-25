import pygame
from PIL import Image
import time
import pandas as pd
import math
canteen_data = pd.read_excel("canteens.xlsx")

#function to create a list of all the keywords from the excel sheet, to be used later in mains in both options 2 and 3
def load_all_keywords_list(data_location="canteens.xlsx"): 
    keyword_data = pd.read_excel(data_location)
    list_keyword1 = keyword_data['Keywords'].tolist() #list of all the column
    list_keyword1 = [i.replace(', ', '#') for i in list_keyword1]
    list_keyword2 = [i.split('#') for i in list_keyword1]
    list_keyword3 = sum(list_keyword2, [])
    list_keyword = [x.lower() for x in list_keyword3]

    return list_keyword


#function to ensure keywords input results in an output, will be used in main later to  ensure validity of keywords in both options 2 and 3
def keywords_checker(user_input): 
    user_input1 = user_input.replace('mixed rice','mr')
    
    
    if ' or ' in user_input1:
        user_input2 = user_input1.split(' or ')
        user_input3 = list(map(lambda x: x if x != 'mr' else 'mixed rice', user_input2))
        return any(x in user_input3 for x in load_all_keywords_list()) #returns true if any element in user input list exists in list of keywords
    

    elif ' and ' in user_input1 or ' ' in user_input1:
        user_input2 = user_input1.replace(' and ', ' ')
        user_input3 = user_input2.split(' ')
        user_input4 = list(map(lambda x: x if x != 'mr' else 'mixed rice', user_input3))
        return all(x in load_all_keywords_list() for x in user_input4) #returns true if all elements in user input list exists in list of keywords

    else:
        user_input2 = user_input1.replace('mr','mixed rice')
        if user_input2 in load_all_keywords_list():
            return True #returns true if element exist in keywords list

#function to ensure keywords do not have both and and or, will be used both in options 2 and 3 later
def both_and_orchecker(user_input): 
    keyword_user_input1 = user_input.replace('mixed rice', 'mixed_rice')
    
    if ' and ' in user_input and ' or ' in user_input:
        print("Please only key in in AND or OR, not both")
        return not True

    
    
    elif ' or ' in keyword_user_input1: #do not want to accept case where both space and or are used
        Listed_words= keyword_user_input1.split(' or ')
        Listed_words_string = ''.join(Listed_words)
        if ' ' in Listed_words_string:
            print("Please key in only OR or space/and, not both")
            return not True
        else: return True

    else: return True
    
        
#function to ensure keywords keyed in are not empty, will be used in both options 2 and 3 later
def length_checker(user_input): 
    if len(user_input) == 0:
        Print('Please key in something')
        return not True
    else:
        return True



def load_stall_keywords(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    keywords = {}
    for canteen in canteens:
        keywords[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_keywords_intermediate = copy.set_index('Stall')['Keywords'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_keywords = stall_keywords_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        keywords[stall_canteen][stall] = stall_keywords

    return keywords
overall_dictionary = load_stall_keywords() #calling the function above globally to get a dictionary containing locations and their respective stalls and stalls and their respective keywords, will be used in the following function


#the function below will be used for options 1 and 2 of the code
def final_search(keyword): #nested function that returns output in terms of 1)Count and 2)List of stalls matching the keyword for each keyword
        count_keywordstalls = 0 #initial count of stalls matching keyword set to 0
        stalls_list = [] # defining a list that will output all the stalls and their locations later
        for location in overall_dictionary: # for every location in the earlier dictionary
            stalls_keywords = overall_dictionary[location] # dictionary of stalls and their keywords excluding the location
            for stall in stalls_keywords: #checking if the stalls have the keyword we are looking for
                listed_keywords = stalls_keywords[stall].lower().split(', ') #list of keyword for each stall
                if keyword in listed_keywords:
                    count_keywordstalls += 1
                    stalls_list.append( location + ' - ' + stall)
        return count_keywordstalls, stalls_list #function returns total count and stalls
    


#overall function that gives output once called with keywords_input inside
def search_by_keyword(keywords_input): 
    keywords_input1 = keywords_input.replace('mixed rice','mixed_rice') #mixed rice case only needs to be accounted for in and scenario
    
    if ' or ' in keywords_input: #or is used in keyword. Or is solved first to ensure that the blank spaces in the elif statements are not from OR inputs
        keywords_inputresolved = keywords_input.split(' or ') #replace or and split words into a list
        keywords_inputresolved1 = [] 
        for key in keywords_inputresolved: #handling accidental miltiple spaces added by the user
            key.replace(' ','')
            keywords_inputresolved1.append(key)
        stalls = []
        for key in keywords_inputresolved1: 
            stalls.append((final_search(key)[1])) #makes a list of all the stalls found from each keyword by calling the final search function defined earlier
        all_stalls = sum(stalls, []) #makes a lengthed list of all the stalls involved with all keywords, note this part will have repeated stalls based on their number of occurences
        occurrence_list = []
        for each_stall in all_stalls: #count occurrence of each stall and make it into a list
            occurrence_list.append(all_stalls.count(each_stall))
        occurrence_dictionary = dict(zip(all_stalls, occurrence_list)) #makes a dictionary with each stall and its occurrence with respect to the keywords, this no longer has duplicates due to the dictionary function of unique keys
        numbers_list = [] #we need to output stalls that match each of the numbers of keywords in this list
        for stall_counted in occurrence_dictionary: #outputs list of numbers(each number signifying occurence)
            if occurrence_dictionary[stall_counted] not in numbers_list:
                numbers_list.append(occurrence_dictionary[stall_counted])
        numbers_list.sort(reverse = True) #priority given to stalls that meet most keywords

        if len(occurrence_dictionary) != 0: #check if any stall are found
            print('Stalls Found = ' + str(len(occurrence_dictionary)))
        else:
            print('No food stall found with input keyword, please try again')
            
            
        for number in numbers_list: #final output for OR keyword
            print('\nStalls that match ' + str(number) + ' keyword/s:')
            for each_stall in occurrence_dictionary: #prints each set of occurrence
                if occurrence_dictionary[each_stall] == number:
                    print(each_stall)

    elif ' and ' or ' ' in keywords_input1: #and or space is used in keyword
        keywords_inputresolved1 = keywords_input1.replace(' and ', '#') #replace and with # to split later
        keywords_inputresolved2 = keywords_inputresolved1.replace(' ', '#') #to split later and to account for mixed rice
        keywords_inputresolved3 = keywords_inputresolved2.replace('mixed_rice', 'mixed rice')
        
        keywords_inputresolved = keywords_inputresolved3.split('#') #replace and split words seperated by space into a list
        stalls = []
        for key in keywords_inputresolved: 
            stalls.append((final_search(key)[1])) #makes a list of all the stalls found from each keyword by calling the final search function defined earlier\
        all_stalls = sum(stalls, []) #makes a lengthed list of all the stalls involved with all keywords
        final_stalls_list = [] #final stalls list to be found
        for each_stall in all_stalls: #only input in stalls that satisfy all three keywords
            if all_stalls.count(each_stall) == len(keywords_inputresolved) and each_stall not in final_stalls_list:
                final_stalls_list.append(each_stall)
        if len(final_stalls_list) != 0:
            print('Stalls Found = ' + str(len(final_stalls_list)))
            
        else:
            print('No food stall found with input keyword, please try again')
            
        for stall in final_stalls_list:
            print(stall)
        

    else: # final condition where etiher one keyword is keyed in or invalid input
        stalls = final_search(keywords_input[1])
        if final_search(keywords_input[0])== 0:
            print('No food stall found with input keyword, please try again')
            
        else:
            print('Stalls Found = ' + str(final_search(keywords_input[0])))
            for stall in stalls:
                print(stall)
        

#load dataset for price dictionary - provided
def load_stall_prices(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    prices = {}
    for canteen in canteens:
        prices[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_prices_intermediate = copy.set_index('Stall')['Price'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_price = stall_prices_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        prices[stall_canteen][stall] = stall_price

    return prices       
        
        
overall_price = load_stall_prices()


def search_by_price(keywords_input, max_price):
    keywords_input1 = keywords_input.replace('mixed rice','mixed_rice') #mixed rice case only needs to be accounted for in and scenario
    
    all_stalls = [] #first part of this code is similar to part 1 where we try to output all the respective stalls related to the respective input
    if ' or ' in keywords_input:
        stalls = []
        keywords_inputresolved = keywords_input.split(' or ')
        for key in keywords_inputresolved: 
            stalls.append((final_search(key)[1])) #makes a list of all the stalls found from each keyword by calling the final search function defined earlier\
        all_stalls.append(sum(stalls, [])) #makes a lengthed list of all the stalls involved with all keywords

    elif ' and ' or ' ' in keywords_input1: #and or space is used in keyword
        
        keywords_inputresolved1 = keywords_input1.replace(' and ', '#') #replace and with # to split later
        keywords_inputresolved2 = keywords_inputresolved1.replace(' ', '#') #to split later and to account for mixed rice
        keywords_inputresolved3 = keywords_inputresolved2.replace('mixed_rice', 'mixed rice')
        
        keywords_inputresolved = keywords_inputresolved3.split('#') #replace and split words seperated by space into a list
        stalls = []
        for key in keywords_inputresolved: 
            stalls.append((final_search(key)[1])) #makes a list of all the stalls found from each keyword by calling the final search function defined earlier\
        all_stalls1 = sum(stalls, []) #makes a lengthed list of all the stalls involved with all keywords
        final_stalls_list = [] #final stalls list to be found
        for each_stall in all_stalls1: #only input in stalls that satisfy all three keywords
            if all_stalls1.count(each_stall) == len(keywords_inputresolved) and each_stall not in final_stalls_list:
                final_stalls_list.append(each_stall)
        all_stalls.append(final_stalls_list)
        
        
    else: all_stalls.append(final_search(keywords_input[1]))

    all_stalls2 = sum(all_stalls, []) #lengthened list of everything
    all_stalls_resolved = [] #list with no duplicates
    for stall in all_stalls2:
        if stall not in all_stalls_resolved:
            all_stalls_resolved.append(stall)
    price_list = [] #defining two lists to create a dictionary later
    name_list = []
    for location in overall_price: # for every location in the earlier dictionary
        stalls_price = overall_price[location]
        for stall in stalls_price: #making a list of stalls and their prices each
                price_list.append(stalls_price[stall])
                name_list.append(location + ' - ' + stall)
    location_price_dictionary = dict(zip(name_list, price_list))

    stalls_found = []  #searching for stalls that are below the max price
    for stall in all_stalls_resolved:
        if location_price_dictionary[stall] <= max_price:
            stalls_found.append(stall)

    price_list_chosen = [] #price list for stalls output

    for stall in stalls_found:
        price_list_chosen.append(location_price_dictionary[stall])

    chosen_stalls_dict = dict(zip(stalls_found, price_list_chosen))
    
    chosen_stalls_dict_sorted = {k: v for k, v in sorted(chosen_stalls_dict.items(), key=lambda item: item[1])}

    

    if len(stalls_found) != 0: #as long as there is a result within this price range
        print( 'Stalls Found: ' + str(len(stalls_found)))
        for stall in chosen_stalls_dict_sorted:
            print(stall + ' - $' + "{:.2f}".format(chosen_stalls_dict_sorted[stall]))

    else:
        if len(all_stalls_resolved) == 0: #no stalls found with the keywords used
            print('Please enter a valid keyword input')

        else:
            print('No stall found within the price range. Here is a recommendation based on proximity to price range : ')
            chosen_stall = ''
            initial_price = 15 #max price in sheet
            for stall in all_stalls_resolved:
                if location_price_dictionary[stall] < initial_price:
                    chosen_stall = stall
                    initial_price = location_price_dictionary[stall]
            print(chosen_stall + ' $' + "{:.2f}".format(initial_price))




                 
# load dataset for location dictionary - provided
def load_canteen_location(data_location="canteens.xlsx"):
    # get list of canteens
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    # get dictionary of {canteen:[x,y],}
    canteen_locations = {}
    for canteen in canteens:
        copy = canteen_data.copy()
        copy.drop_duplicates(subset="Canteen", inplace=True)
        canteen_locations_intermediate = copy.set_index('Canteen')['Location'].to_dict()
    for canteen in canteens:
        canteen_locations[canteen] = [int(canteen_locations_intermediate[canteen].split(',')[0]),
                                      int(canteen_locations_intermediate[canteen].split(',')[1])]

    return canteen_locations


# get user's location with the use of PyGame - provided
def get_user_location_interface():
    # get image dimensions
    image_location = 'NTUcampus.jpg'
    pin_location = 'pin.png'
    screen_title = "NTU Map"
    image = Image.open(image_location)
    image_width_original, image_height_original = image.size
    scaled_width = int(image_width_original)
    scaled_height = int(image_height_original)
    pinIm = pygame.image.load(pin_location)
    pinIm_scaled = pygame.transform.scale(pinIm, (60, 60))
    # initialize pygame
    pygame.init()
    # set screen height and width to that of the image
    screen = pygame.display.set_mode([scaled_width, scaled_height])
    # set title of screen
    pygame.display.set_caption(screen_title)
    # read image file and rescale it to the window size
    screenIm = pygame.image.load(image_location)

    # add the image over the screen object
    screen.blit(screenIm, (0, 0))
    # will update the contents of the entire display window
    pygame.display.flip()

    # loop for the whole interface remain active
    while True:
        # checking if input detected
        pygame.event.pump()
        event = pygame.event.wait()
        # closing the window
        if event.type == pygame.QUIT:
            pygame.display.quit()
            mouseX_scaled = None
            mouseY_scaled = None
            break
        # resizing the window
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(screenIm, event.dict['size']), (0, 0))
            scaled_height = event.dict['h']
            scaled_width = event.dict['w']
            pygame.display.flip()
        # getting coordinate
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get outputs of Mouseclick event handler
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # paste pin on correct position
            screen.blit(pinIm_scaled, (mouseX - 25, mouseY - 45))
            pygame.display.flip()
            # return coordinates to original scale
            mouseX_scaled = int(mouseX * 1281 / scaled_width)
            mouseY_scaled = int(mouseY * 1550 / scaled_height)
            # delay to prevent message box from dropping down
            time.sleep(0.2)
            break

    pygame.quit()
    pygame.init()
    return mouseX_scaled, mouseY_scaled

canteen_locations = load_canteen_location("canteens.xlsx")

#This functions sorts distance in order of distance from midpoint. This method is chosen as based on my experience in NTU, I prefer meeting my friends somewhere which is as convenient for both of us, the midpoint
def search_nearest_canteens(user_locations, k): 
    avg_location = [(user_locations[0][0] + user_locations[1][0])/2,(user_locations[0][1] + user_locations[1][1])/2] #returns the avg user location
    canteens = []
    distance_from_loc = []
    for canteen in canteen_locations: #forming a dictionary of each location and distance from user
        canteens.append(canteen)
        distance_squared = (avg_location[1] - canteen_locations[canteen][1])**2 + (avg_location[0] - canteen_locations[canteen][0])**2
        distance = math.sqrt(distance_squared)
        distance_from_loc.append(distance)
    dictionary_loc = dict(zip(canteens, distance_from_loc))
    
    distance_from_loc.sort() #sorting the distances in ascending orders
    final_distance = distance_from_loc[0:k] #only takes in the k distances
    canteens_near =[] #finding canteens respective to the distance found
    for distance in final_distance: #finding canteens respective to the distance found 
        for canteen in dictionary_loc:
            if dictionary_loc[canteen] == distance:
                canteens_near.append(canteen)

    dictionary_final = dict(zip(canteens_near, final_distance)) #FINAL dictionary with k stalls
 
    print(str(k) + ' Nearest Canteens Found')

    for distance in final_distance:
        for canteen in dictionary_final:
            if dictionary_final[canteen] == distance:
                print(canteen + ' - ' + str(int(distance)) + 'm from midpoint of distances')
        

def main():
    loop = True

    while loop:
        print("=======================")
        print("F&B Recommendation Menu")
        print("1 -- Display Data")
        print("2 -- Keyword-based Search")
        print("3 -- Price-based Search")
        print("4 -- Location-based Search")
        print("5 -- Exit Program")
        print("=======================")
        #print(get_user_location_interface())

        

        option1 = input("Enter option [1-5]: ")

        if option1.isnumeric() == True:
            option = int(option1)


            if option == 1:
                #print provided dictionary data structures
                print("1 -- Display Data")
                print("Keyword Dictionary: ", overall_dictionary)
                print("Price Dictionary: ", overall_price)
                print("Location Dictionary: ", canteen_locations)
            elif option == 2:
                keyword_user_input = (input('Please enter the keywords required, you may key in AND, a space or an OR : ')).lower()
                while keywords_checker(keyword_user_input.lower()) != True or both_and_orchecker(keyword_user_input.lower()) != True or length_checker(keyword_user_input.lower()) != True : #making sure keywords are valid based on functions defined earlier
                    print('Invalid user input, please try again')
                    keyword_user_input = input('Please enter the keywords required, you may key in AND, a space or an OR : ').lower()
                    
                search_by_keyword(keyword_user_input.lower()) #calls the search function

            elif option == 3:
                keyword_user_input = (input('Please enter the keywords required, you may key in AND, a space or an OR : ')).lower()

                while keywords_checker(keyword_user_input.lower()) != True or both_and_orchecker(keyword_user_input.lower()) != True or length_checker(keyword_user_input.lower()) != True : #making sure keywords are valid based on functions defined earlie
                    print('Invalid user input, please try again')
                    keyword_user_input = input('Please enter the keywords required, you may key in AND, a space or an OR : ').lower()
                        
                price_input = (input('Please key in the max price you are willing to pay. Please key in positive NUMBERS only : '))
                price_checker = price_input.replace('.','').isnumeric()
                while price_checker == False: 
                    print('Please enter a positive number only')
                    price_input = (input('Please key in the max price you are willing to pay. Please key in positive NUMBERS only : '))
                    price_checker = price_input.replace('.','').isnumeric()
                
                price_max = float(price_input)
                search_by_price(keyword_user_input.lower(), price_max) 
                    
            elif option ==4:
                k = input('Please enter the number of canteens you are looking for: ')
                user_A = get_user_location_interface()
                user_B = get_user_location_interface()
                print('User A\'s location (x,y): ' + str(user_A))
                print('User B\'s location (x,y): ' + str(user_B))
                user_locations = []
                user_locations.append(user_A)
                user_locations.append(user_B)
                try:
                    K = int(k)
                    if K < 0 or K >15:
                        print('K cannot be negative or more than 15 as there are only 15 locations. Default K = 1 is set')
                        search_nearest_canteens(user_locations, 1)
                    else:
                        search_nearest_canteens(user_locations, K)
                except:
                    print('Please enter a valid integer as input, default K set to 1')
                    search_nearest_canteens(user_locations, 1)
                    
            elif option ==5:
                #exit the program
                print("Exiting F&B Recommendation")
                loop = False

            else: continue

        else: continue

        
            

main()


