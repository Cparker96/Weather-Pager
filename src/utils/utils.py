from logger.logger import logger

def subscribe_by_state(available_states: list[str]) -> list[str]:
    while True:
        states_input = input("What states are you interested in getting weather events for? Please submit in the form of a list of comma separated values (case sensitive): ")
        if len(states_input) == 0:
            continue

        states_list = states_input.split(",")
        invalid_state_found = False

        for state in states_list:
            if state not in available_states:
                logger.info(f"Your state selection '{state}' is not in the list of available state names (50 US States). Check the spelling or verify its an applicable name")
                invalid_state_found = True
                break
        
        # re-evaluate the input if an invalid state is given
        if invalid_state_found:
            continue

        return states_list
    
def subscribe_by_event(available_weather_events: list[str]) -> list[str]:
    while True:
        events_input = input("What weather topics are you interested in getting weather events for? Please submit in the form of a list of comma separated values (case sensitive). Options are 'drought','dustHaze','earthquakes','floods','landslides','manmade','seaLakeIce','severeStorms','snow','tempExtremes','volcanoes','waterColor', and 'wildfires' \n")
        if len(events_input) == 0:
            continue

        events_list = events_input.split(",")
        invalid_event_found = False

        for event in events_list:
            if event not in available_weather_events:
                logger.info(f"Your weather event selection '{event}' is not in the list of available weather events. Check the spelling or verify its an applicable name")
                invalid_event_found = True
                break

        # re-evaluate the input if an invalid event is given
        if invalid_event_found:
            continue

        return events_list


available_states = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming"
]

available_weather_events = [
    "drought",
    "dustHaze",
    "earthquakes",
    "floods",
    "landslides",
    "manmade",
    "seaLakeIce",
    "severeStorms",
    "snow",
    "tempExtremes",
    "volcanoes",
    "waterColor",
    "wildfires"
]