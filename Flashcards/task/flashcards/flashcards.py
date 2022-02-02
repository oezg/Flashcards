import random
import json
import logging
import shutil
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(description="This program is a flashcards application.")
parser.add_argument('-i', '--import_from',
                    help="Enter the name of the json file from which flashcards can be imported.")
parser.add_argument('-e', '--export_to',
                    help='Enter the name of the file to which flashcards will be saved at the end.')
arguments = parser.parse_args()

logging.basicConfig(format="%(message)s", level="DEBUG", filemode='w', filename='logfile.txt')
cards = {}
errors = defaultdict(int)


def log(message: str):
    logging.info(message)
    print(message)
    

def log_input(message: str) -> str:
    log(message)
    inp = input()
    logging.info(inp)
    return inp


def add_card():
    term = log_input("The card:")
    while term in cards:
        term = log_input(f'The card "{term}" already exists. Try again:')
    defn = log_input("The definition of the card:")
    while defn in cards.values():
        defn = log_input(f'The definition "{defn}" already exists. Try again:')
    cards.update({term: defn})
    log(f'The pair ("{term}":"{defn}") has been added.')


def remove_card():
    term = log_input("Which card?")
    try:
        cards.pop(term)
    except KeyError:
        log(f'Can\'t remove "{term}": there is no such card.')
    else:
        log('The card has been removed.')


def import_from(filename):
    try:
        with open(filename, "r") as file:
            imported_cards = json.load(file)
    except FileNotFoundError:
        log("File not found.")
    else:
        cards.update(imported_cards)
        log(f"{len(imported_cards)} cards have been loaded.")


def import_from_file():
    filename = log_input("File name:")
    import_from(filename)


def export_to(filename):
    with open(filename, "w") as file:
        json.dump(cards, file)
    log(f"{len(cards)} cards have been saved.")


def export_to_file():
    filename = log_input("File name:")
    export_to(filename)


def ask():
    number = int(log_input("How many times to ask?"))
    for _ in range(number):
        question = random.choice(list(cards))
        answer = log_input(f'Print the definition of "{question}":')
        if answer == cards[question]:
            log("Correct!")
        else:
            errors[question] += 1
            if answer in cards.values():
                correct_answer = ""
                for term, defn in cards.items():
                    if answer == defn and term != question:
                        correct_answer = term
                        break
                log(f'Wrong. The right answer is "{cards[question]}", '
                    f'but your definition is correct for "{correct_answer}".')
            else:
                log(f'Wrong. The right answer is "{cards[question]}".')


def log_to_file():
    filename = log_input("File name:")
    log("The log has been saved.")
    shutil.copy('logfile.txt', filename)


def hardest_card():
    if errors:
        highest_error = max(errors.values())
        hardest_cards = [card for card, error in errors.items() if error == highest_error]
        if len(hardest_cards) > 1:
            hardest_terms = '", "'.join(hardest_cards)
            log(f'The hardest card is "{hardest_terms}". You have {highest_error} errors answering them')
        else:
            log(f'The hardest card is "{hardest_cards[0]}". You have {highest_error} errors answering it')
    else:
        log("There are no cards with errors.")


def reset_stats():
    errors.clear()
    log('Card statistics have been reset.')


def main():
    if arguments.import_from:
        import_from(arguments.import_from)
    action = ""
    while action != "exit":
        action = log_input("Input the action (add, remove, import, export, ask, exit, "
                           "log, hardest card, reset stats):")
        if action == "add":
            add_card()
        elif action == "remove":
            remove_card()
        elif action == "import":
            import_from_file()
        elif action == "export":
            export_to_file()
        elif action == "ask":
            ask()
        elif action == "log":
            log_to_file()
        elif action == "hardest card":
            hardest_card()
        elif action == "reset stats":
            reset_stats()
    else:
        if arguments.export_to:
            export_to(arguments.export_to)
        else:
            log("Bye bye!")


if __name__ == '__main__':
    main()
