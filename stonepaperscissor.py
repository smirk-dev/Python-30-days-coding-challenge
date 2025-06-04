import random
def get_computer_choice():
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)
def get_winner(player, computer):
    if player == computer:
        return "It's a tie!"
    elif (player == 'rock' and computer == 'scissors') or \
            (player == 'scissors' and computer == 'paper') or \
            (player == 'paper' and computer == 'rock'):
        return "You win!"
    else:
        return "Computer wins!"
def rock_paper_scissors():
    print("Welcome to Rock, Paper, Scissors!")
    print("Type 'rock', 'paper', or 'scissors' to play. Type 'quit' to exit.")
    while True:
        player_choice = input("Your choice: ").lower()
        if player_choice == 'quit':
            print("Thanks for playing! Goodbye.")
            break
        if player_choice not in ['rock', 'paper', 'scissors']:
            print("Invalid choice. Please choose rock, paper, or scissors.")
            continue
        computer_choice = get_computer_choice()
        print(f"Computer chose: {computer_choice}")

        result = get_winner(player_choice, computer_choice)
        print(result)
if __name__ == "__main__":
    rock_paper_scissors()
