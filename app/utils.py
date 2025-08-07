import re
from difflib import get_close_matches
import json

def load_bus_data():
    with open('app/bus_timings.json') as f:
        return json.load(f)

def search_buses(query: str):
    buses = load_bus_data()
    query = query.lower().strip()
    
    # Handle common aliases and misspellings
    aliases = {
        'tpt': 'tirupati',
        'hyd': 'hyderabad',
        'bglr': 'bangalore',
        'chen': 'chennai',
        'tirupsathi': 'tirupati',
        'tirupsthi': 'tirupati',
        'hyderabad': 'hyderabad',
        'banglore': 'bangalore'
    }
    query = aliases.get(query, query)
    
    # Find best matches
    route_names = [bus['route'].lower() for bus in buses]
    matches = get_close_matches(query, route_names, n=5, cutoff=0.6)
    
    results = []
    for bus in buses:
        if bus['route'].lower() in matches:
            # Format times consistently
            formatted_times = []
            for time in bus['departure_times']:
                # Convert "HH:MM" format to 12-hour clock
                if re.match(r'^\d{1,2}:\d{2}$', time):
                    hour, minute = map(int, time.split(':'))
                    period = 'AM' if hour < 12 else 'PM'
                    hour = hour % 12 or 12
                    formatted_times.append(f"{hour}:{minute:02d} {period}")
                else:
                    formatted_times.append(time)
            bus['formatted_times'] = formatted_times
            results.append(bus)
    
    return results