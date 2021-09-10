from random import randint
import sqlite3
conn = sqlite3.connect('Jokes.sqlite')
cur = conn.cursor()
used_knock_ids = set()
used_dong_ids = set()


def get_joke(num_of_jokes, type_of_joke):
    print_type = str(type_of_joke).replace('_','-')
    id_set = eval('used_'+ type_of_joke.split('_')[1] + '_ids')
    if len(id_set) == num_of_jokes:
        print(f"Oh no! we're out of {print_type} jokes, feel free to add new ones\n")
        main_knock_dong(type_of_joke)
    id = randint(1, num_of_jokes)
    if id not in id_set:
        id_set.add(id)
        whos_there = str(cur.execute(f'SELECT whos_there FROM {type_of_joke} WHERE id = {id}').fetchone()).strip("'(,)'")
        who = str(cur.execute(f'SELECT who FROM {type_of_joke} WHERE id = {id}').fetchone()).strip("'(,)'")

        print(f"\n{print_type.capitalize()}\nWho's there?\n{whos_there}\n{whos_there} who?\n{who}")
    else:
        get_joke(num_of_jokes, type_of_joke)
    inp = input('\nANOTHER ONE? press Enter, press 0 to exit\n')
    if inp == '0':
        conn.commit()
        conn.close()
        exit()
    get_joke(num_of_jokes, type_of_joke)


def add_joke(type_of_joke):
    print_type = str(type_of_joke).replace('_','-')
    print(f'\n ADD {print_type.upper()} JOKE:\n')
    print('Finish the sentence!')
    whos_there = input(f"{print_type}. Who's there? ")
    who = input(f"{whos_there} who? ")

    cur.execute(f'INSERT INTO {type_of_joke} (whos_there, who) VALUES (?,?);',(whos_there, who))
    print('addition was sucessful!!\n')
    main_knock_dong(type_of_joke)

def main_knock_dong(type_of_joke):
    print_type = str(type_of_joke).replace('_','-')
    main_menu = (f'1. Show me a {print_type} joke!', f'2. add a {print_type} joke', '3. Return to home screen', '0. Exit')
    print(*main_menu, sep='\n')
    user_input = int(input())
    if user_input == 1:
        cur.execute(f'SELECT * FROM {type_of_joke}')
        rows = cur.fetchall()
        num_of_jokes = len(rows)
        get_joke(num_of_jokes, type_of_joke)    
    elif user_input == 2:
        add_joke(type_of_joke)
    elif user_input == 3:
        main()
    elif user_input == 0:
        print('\nBye!')
        conn.commit()
        conn.close()
        exit()
    else:
        print('Only enter a number between 0 and 3\n')
        main_knock_dong(type_of_joke)

def main():
    main_menu = ('1  Knock-knock jokes :)', '2. Ding-dong jokes ;)', '0. Exit')
    print(*main_menu, sep='\n')
    user_input = int(input())
    if user_input == 1:
        main_knock_dong('knock_knock')
    elif user_input == 2:
        main_knock_dong('ding_dong')
    elif user_input == 0:
        conn.commit()
        conn.close()
        print('\nBye!')
    else:
        print('Only enter a number between 0 and 2\n')
        main()
main()    
conn.commit()
conn.close()