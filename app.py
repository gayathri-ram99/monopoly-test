import json

# Load board from JSON
with open('/Users/gayathriramachandran/Downloads/new_coding_test/board.json') as f:
    board = json.load(f)


# Function to load rolls
def load_rolls(filename):
    with open(filename) as f:
        return json.load(f)


# Choose rolls file
rolls_choice = input("Enter 1 for rolls_1.json or 2 for rolls_2.json: ")
rolls_file = '/Users/gayathriramachandran/Downloads/new_coding_test/rolls_1.json' if rolls_choice == '1' else '/Users/gayathriramachandran/Downloads/new_coding_test/rolls_2.json'
rolls = load_rolls(rolls_file)

# Player setup
players = [
    {"name": "Peter", "money": 16, "position": 0, "properties": []},
    {"name": "Billy", "money": 16, "position": 0, "properties": []},
    {"name": "Charlotte", "money": 16, "position": 0, "properties": []},
    {"name": "Sweedal", "money": 16, "position": 0, "properties": []},
]


# Helper function to get property owner
def get_owner(property_name):
    for player in players:
        if property_name in player["properties"]:
            return player
    return None


# Game loop
turn = 0
while rolls:
    player = players[turn % 4]  # Rotate turns
    roll = rolls.pop(0)  # Get the next dice roll

    # Move player
    prev_position = player["position"]
    player["position"] = (player["position"] + roll) % len(board)
    landed = board[player["position"]]

    # Passing GO rule
    if player["position"] < prev_position:
        player["money"] += 1

    # Handle property
    if landed["type"] == "property":
        owner = get_owner(landed["name"])
        if owner is None:
            if player["money"] >= landed["price"]:
                player["money"] -= landed["price"]
                player["properties"].append(landed["name"])
        elif owner != player:
            same_colour = [p for p in board if p.get("colour") == landed["colour"]]
            owned_same_colour = all(p["name"] in owner["properties"] for p in same_colour)
            rent = landed["price"] * (2 if owned_same_colour else 1)
            player["money"] -= rent
            owner["money"] += rent

            # Bankruptcy check
            if player["money"] < 0:
                print(f"{player['name']} is bankrupt! Game over.")
                break

    # Move to next turn
    turn += 1

# Determine the winner
winner = max(players, key=lambda p: p["money"])
print(f"Winner: {winner['name']} with ${winner['money']}")
