from InputParser import parse_input_file
from Slots import GameSlot, PracticeSlot

def create_game_and_practice_slots(game_slots, practice_slots):
    # Mapping of day abbreviations to duplications
    game_duplications = {
        "MO": ["WE", "FR"],
        "TU": ["TH"],
    }
    practice_duplications = {
        "MO": ["WE"],
        "TU": ["TH"],
    }

    # Function to create slots and apply duplications
    def duplicate_slots(slot_dict, slot_class, duplications):
        slot_objects = {}
        for slot_key, slot_data in slot_dict.items():
            day, time = slot_key.split()
            max_val = slot_data["max"]
            min_val = slot_data["min"]

            # Create the primary slot
            slot = slot_class(max_val, min_val, day, time)
            slot_objects[f"{day} {time}"] = slot

            # Create duplicate slots for specified days
            for new_day in duplications.get(day, []):
                duplicate_slot = slot_class(max_val, min_val, new_day, time)
                slot_objects[f"{new_day} {time}"] = duplicate_slot

        return slot_objects

    # Create and duplicate GameSlot objects
    game_slot_objects = duplicate_slots(game_slots, GameSlot, game_duplications)

    # Create and duplicate PracticeSlot objects
    practice_slot_objects = duplicate_slots(practice_slots, PracticeSlot, practice_duplications)

    return game_slot_objects, practice_slot_objects


if __name__ == "__main__":
    # Parse the input file
    (
        game_slots, practice_slots, games, practices, not_compatible,
        unwanted, preferences, pair, partial_assignments, wminfilled, 
        wpref, wpair, wsecdiff, pengamemin, penpracticemin,
        pennotpaired, pensection
    ) = parse_input_file()

    # Create GameSlot and PracticeSlot objects
    game_slot_objects, practice_slot_objects = create_game_and_practice_slots(game_slots, practice_slots)

    # Print created slots for verification
    print("Game Slots:")
    for slot_key, slot in game_slot_objects.items():
        print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")

    print("\nPractice Slots:")
    for slot_key, slot in practice_slot_objects.items():
        print(f"{slot.day} {slot.startTime} -> Max: {slot.max}, Min: {slot.min}")

    print("\nGames:")
    for game in games:
        print(f"  {game}")

    print("\nPractices:")
    for practice in practices:
        print(f"  {practice}")

    print("\nNot Compatible:")
    for pair in not_compatible:
        print(f"  {pair}")

    print("\nUnwanted:")
    for key, identifiers in unwanted.items():
        print(f"  {key} -> {', '.join(identifiers)}")

    print("\nPreferences:")
    for key, value in preferences.items():
        print(f"  {key} -> {value}")

    print("\nPair:")
    for pair_value in pair:
        print(f"  {pair_value}")

    print("\nPartial Assignments:")
    for key, identifiers in partial_assignments.items():
        print(f"  {key} -> {', '.join(identifiers)}")

    # Print Weights and Penalty values
    print("\nWeights and Penalty values:")
    print(f"wminfilled: {wminfilled}")
    print(f"wpref: {wpref}")
    print(f"wpair: {wpair}")
    print(f"wsecdiff: {wsecdiff}")
    print(f"pengamemin: {pengamemin}")
    print(f"penpracticemin: {penpracticemin}")
    print(f"pennotpaired: {pennotpaired}")
    print(f"pensection: {pensection}")