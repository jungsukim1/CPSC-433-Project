import sys
from collections import defaultdict

def parse_input_file():
    input_file = sys.argv[1]

    # Variables for each section
    game_slots = {}
    practice_slots = {}
    games = []
    practices = []
    not_compatible = set()
    unwanted = defaultdict(list)
    preferences = defaultdict(dict)
    pair = set()
    partial_assignments = defaultdict(list)

    # Variables for weightings and penalties
    wminfilled = 0.0
    wpref = 0.0
    wpair = 0.0
    wsecdiff = 0.0
    pengamemin = 0
    penpracticemin = 0
    pennotpaired = 0
    pensection = 0

    current_section = None

    # Open and parse the input file
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()  # Remove extra whitespace
            if not line:  # Skip empty lines
                continue
            elif line == "Game slots:":
                current_section = "game_slots"
            elif line == "Practice slots:":
                current_section = "practice_slots"
            elif line == "Games:":
                current_section = "games"
            elif line == "Practices:":
                current_section = "practices"
            elif line == "Not compatible:":
                current_section = "not_compatible"
            elif line == "Unwanted:":
                current_section = "unwanted"
            elif line == "Preferences:":
                current_section = "preferences"
            elif line == "Pair:":
                current_section = "pair"
            elif line == "Partial assignments:":
                current_section = "partial_assignments"
            else:
                # Process data based on the current section
                if current_section == "game_slots" or current_section == "practice_slots":
                    # Parse slot data and use "Day StartTime" as the key
                    day, start_time, max_val, min_val = map(str.strip, line.split(","))
                    if current_section == "game_slots":
                        game_slots[f"{day} {start_time}"] = {
                            "max": int(max_val),
                            "min": int(min_val)
                        }
                    else:
                        practice_slots[f"{day} {start_time}"] = {
                            "max": int(max_val),
                            "min": int(min_val)
                        }
                elif current_section == "games":
                    games.append(line.strip())
                elif current_section == "practices":
                    practices.append(line.strip())
                elif current_section == "not_compatible":
                    not_compatible.add(tuple(map(str.strip, line.split(","))))
                elif current_section == "unwanted":
                    identifier, day, time = map(str.strip, line.split(","))
                    unwanted[f"{day} {time}"].append(identifier)
                elif current_section == "preferences":
                    day, time, identifier, value = map(str.strip, line.split(","))
                    preferences[f"{day} {time} {identifier}"] = float(value)
                elif current_section == "pair":
                    pair.add(tuple(map(str.strip, line.split(","))))
                elif current_section == "partial_assignments":
                    identifier, day, time = map(str.strip, line.split(","))
                    partial_assignments[f"{day} {time}"].append(identifier)

    # Extracting weights and penalties from the command-line arguments
    if len(sys.argv) < 10:
        raise ValueError(
            "Usage: python script.py <filename> <wminfilled> <wpref> <wpair> <wsecdiff> <pengamemin> <penpracticemin> <pennotpaired> <pensection>"
        )
    
    # Command-line arguments for weightings and penalties
    wminfilled = float(sys.argv[2])
    wpref = float(sys.argv[3])
    wpair = float(sys.argv[4])
    wsecdiff = float(sys.argv[5])
    pengamemin = int(sys.argv[6])
    penpracticemin = int(sys.argv[7])
    pennotpaired = int(sys.argv[8])
    pensection = int(sys.argv[9])

    # Return all variables including the weightings and penalties
    return (
        game_slots, practice_slots, games, practices, not_compatible,
        unwanted, preferences, pair, partial_assignments,
        wminfilled, wpref, wpair, wsecdiff, pengamemin, penpracticemin,
        pennotpaired, pensection
    )