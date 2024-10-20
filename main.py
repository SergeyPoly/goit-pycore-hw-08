from helpers import parse_input
from bot_commands import commands, exit_commands
from serializers import load_data, save_data

def main():
    book = load_data()
    all_commands = ', '.join([command for command in commands] + exit_commands)
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        if command in exit_commands:
            save_data(book)
            print("Good bye!")
            break

        elif command in commands:
            print(commands[command](args, book))
            
        else:
            print(f"Invalid command or no command entered.\nPossible options: {all_commands}.")

if __name__ == "__main__":
    main()