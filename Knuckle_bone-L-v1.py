#!/usr/bin/env python3
import random, time, sys

# Each board has 3 columns (lists of numbers)
player_board = [[], [], []]
bot_board = [[], [], []]

def show_rules():
    print("""
=== KNUCKLEBONES RULES ===
1. Take turns rolling a 6-sided die and placing it in one of 3 columns.
2. Score = Sum of all dice on your board.
3. Combo Multiplier: Matching dice in the same column multiply!
   - Two of the same number = (number + number) x 2
   - Three of the same number = (number + number + number) x 3
4. Attack: Placing a die destroys all dice of that same value in your opponent's opposite column.
5. Game End: The game ends as soon as either player fills all 9 spaces on their board. Highest score wins!
==========================
""")

def get_col_score(col):
    # Counts duplicates in a column and applies the CoTL multiplier
    total = 0
    for die in set(col):
        count = col.count(die)
        total += (die * count) * count
    return total

def get_total_score(board):
    return sum(get_col_score(col) for col in board)

def print_boards():
    # Helper to grab a die or return a blank space if empty
    def cell(board, col, row):
        return board[col][row] if row < len(board[col]) else " "

    print("\n" + "="*25)
    print(f"BOT SCORE: {get_total_score(bot_board)}")
    for r in range(2, -1, -1): # Print bot board upside-down facing the player
        print(f"|  {cell(bot_board, 0, r)}  |  {cell(bot_board, 1, r)}  |  {cell(bot_board, 2, r)}  |")
        print("|_____|_____|_____|")
    
    print("\ncollum1#collum2#collum3")
    for r in range(3):
        print(f"|  {cell(player_board, 0, r)}  |  {cell(player_board, 1, r)}  |  {cell(player_board, 2, r)}  |")
        print("|_____|_____|_____|")
    print(f"YOUR SCORE: {get_total_score(player_board)}")
    print("="*25 + "\n")

def is_board_full(board):
    return all(len(col) == 3 for col in board)

print("Welcome to Knucklebones!")
print("Type 'rule' at any time for instructions, or 'exit' to quit.")

while True:
    print_boards()
    
    # --- PLAYER TURN ---
    D1 = random.randint(1, 6)
    print(f"You rolled: {D1}")
    
    while True:
        R1 = input("Place in (collum1, collum2, collum3), or type 'rule' / 'exit': ").strip().lower()
        
        if R1 == "exit":
            print("Thanks for playing!")
            sys.exit()
        elif R1 == "rule":
            show_rules()
            continue
        elif R1 in ["collum1", "collum2", "collum3"]:
            col_idx = int(R1[-1]) - 1 # Converts 'collum1' to index 0, etc.
            
            if len(player_board[col_idx]) < 3:
                player_board[col_idx].append(D1)
                # Destroy matching dice in the bot's opposite column
                bot_board[col_idx] = [die for die in bot_board[col_idx] if die != D1]
                break
            else:
                print("That column is full! Pick another.")
        else:
            print("Oops, you typed something wrong. Please try again.")

    if is_board_full(player_board):
        break

    # --- BOT TURN ---
    print("\nBot is rolling...")
    time.sleep(1.5)
    bot_die = random.randint(1, 6)
    print(f"Bot rolled: {bot_die}")
    time.sleep(1)

    # Bot picks a random column that isn't full
    open_cols = [i for i in range(3) if len(bot_board[i]) < 3]
    bot_choice = random.choice(open_cols)
    
    bot_board[bot_choice].append(bot_die)
    # Bot destroys matching dice in your opposite column
    player_board[bot_choice] = [die for die in player_board[bot_choice] if die != bot_die]
    print(f"Bot placed {bot_die} in collum{bot_choice + 1}!")
    time.sleep(1)

    if is_board_full(bot_board):
        break

# --- GAME OVER ---
print_boards()
p_final = get_total_score(player_board)
b_final = get_total_score(bot_board)

print("GAME OVER!")
if p_final > b_final:
    print(f"You win! ({p_final} to {b_final})")
elif b_final > p_final:
    print(f"The Bot wins! ({b_final} to {p_final})")
else:
    print(f"It's a tie! ({p_final} to {b_final})")
