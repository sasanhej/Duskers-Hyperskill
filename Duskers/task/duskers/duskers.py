def logo():
    return '''+=======================================================================+
  ######*   ##*   ##*  #######*  ##*  ##*  #######*  ######*   #######*
  ##*  ##*  ##*   ##*  ##*       ##* ##*   ##*       ##*  ##*  ##*
  ##*  ##*  ##*   ##*  #######*  #####*    #####*    ######*   #######*
  ##*  ##*  ##*   ##*       ##*  ##* ##*   ##*       ##*  ##*       ##*
  ######*    ######*   #######*  ##*  ##*  #######*  ##*  ##*  #######*
                      (Survival ASCII Strategy Game)
+=======================================================================+'''


def robots(nrobots=3):
    return f'''
__________(LOG)__________________________________________________(LOG)__________
+==============================================================================+
{'  $   $$$$$$$   $  |'*(nrobots-1)+'  $   $$$$$$$   $  '}
{'  $$$$$     $$$$$  |'*(nrobots-1)+'  $$$$$     $$$$$  '}
{'      $$$$$$$      |'*(nrobots-1)+'      $$$$$$$      '}
{'     $$$   $$$     |'*(nrobots-1)+'     $$$   $$$     '}
{'     $       $     |'*(nrobots-1)+'     $       $     '}
+==============================================================================+
|                  [Ex]plore                          [Up]grade                |
|                  [Save]                             [M]enu                   |
+==============================================================================+
'''


def hub():
    while True:
        print(robots())
        com = input('\nYour command:\n').lower()
        if com == 'ex':
            explore()
            break
        elif com == 'up':
            upgrade()
            break
        elif com == 'save':
            save()
            break
        elif com == 'm':
            gamemenu()
            break
        else:
            print('Invalid input')


def explore():
    comingsoon()


def upgrade():
    comingsoon()


def save():
    comingsoon()


def gamemenu():
    while True:
        print('''[Back] to game\nReturn to [Main] Menu\n[Save] and exit\n[Exit] game''')
        com = input('\nYour command:\n').lower()
        if com == 'back':
            hub()
            break
        elif com == 'main':
            menu()
            break
        elif com == 'save':
            save()
            break
        elif com == 'exit':
            print('\nThanks for playing, bye!\n')
            break
        else:
            print('Invalid input')


def play():
    name = input('\nEnter your name:\n')
    while True:
        print(f'\nGreetings, commander {name}!\nAre you ready to begin?\n    [Yes] [No] Return to Main[Menu]')
        com = input('\nYour command:\n').lower()
        if com == 'yes':
            hub()
            break
        elif com == 'no':
            pass
        elif com == 'menu':
            menu()
            break
        else:
            print('Invalid input')
    exit()


def high():
    while True:
        print("\nNo scores to display.\n	[Back]")
        com = input('\nYour command:\n').lower()
        if com == 'back':
            menu()
            break
        else:
            print('Invalid input')


def helpp():
    comingsoon()


def comingsoon():
    print('Coming SOON! Thanks for playing!')
    exit()

def menu():
    while True:
        print(logo(), '[Play]', '[High] Scores', '[Help]', '[Exit]', sep="\n")
        com = input('\nYour command:\n').lower()
        if com == 'play':
            play()
            break
        elif com == 'high':
            high()
            break
        elif com == 'help':
            helpp()
            break
        elif com == 'exit':
            print('\nThanks for playing, bye!\n')
            break
        else:
            print('Invalid input')


if __name__ == '__main__':
    menu()
