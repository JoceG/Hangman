import random


def game_rules():
    print('{:^80}'.format('WELCOME TO HANGMAN\n'))
    print('1) You have eight guesses')
    print('2) Guess one letter at a time')
    print('3) To guess the phrase, enter "guess" followed by the phrase')
    print('\nNote: none of the inputs are case sensitive.')
    
    enter = input('\n\nPress enter to start the game\n')
    return enter


def create_blanks(chosen):
    blanks = list()
    spaces = list()
    index = 0

    for character in chosen:
        if character.isalpha(): blanks.append('_')
        else: spaces.append(index - len(spaces))
        index += 1

    return blanks, spaces


def print_blanks(blanks_format, spaces):
    capitalize = False
    
    for pos, val in enumerate(blanks_format):
        if pos in spaces:
            print(end='  ')
            capitalize = True

        if capitalize or pos == 0:
            print(val.upper(), end=' ')
            capitalize = False
        else: print(val.lower(), end=' ')

    print('\n')        


def update_blanks(blanks_format, chosen, letter):
    no_spaces = chosen.replace(' ', '')
    
    for pos, val in enumerate(blanks_format):
        if no_spaces[pos] == letter.lower(): blanks_format[pos] = letter

    return blanks_format


def update_image(misses):
    if misses == 0: return [' ' * 10] * 8
    elif misses == 1: return ([' ' * 10] * 7) + ['  ---']
    elif misses == 2: return [' ' * 10] + (['   |'] * 6) + ['  ---']
    elif misses == 3: return ['   ______'] + (['   |'] * 6) + ['  ---']
    elif misses == 4: return ['   ______'] + ['   |    |'] + (['   |'] * 5) + ['  ---']
    elif misses == 5: return ['   ______'] + ['   |    |'] + ['   |   (_)'] + (['   |'] * 4) + ['  ---']
    elif misses == 6: return ['   ______'] + ['   |    |'] + ['   |   (_)'] + ['   |   \|/'] + (['   |'] * 3) + ['  ---']
    elif misses == 7: return ['   ______'] + ['   |    |'] + ['   |   (_)'] + ['   |   \|/'] + ['   |    |'] + (['   |'] * 2) + ['  ---']
    elif misses == 8: return ['   ______'] + ['   |    |'] + ['   |   (_)'] + ['   |   \|/'] + ['   |    |'] + ['   |   / \\'] + ['   |'] + ['  ---']                                                                                          
    else:
        print('\nGame Over. You used all eight guesses.')
        return "Game Over"


def display_image(image):
    print('-' * 52)
    print('{:^52}'.format('HANGMAN STAGE'))
    print()
    
    for line in image: print(line)


def check_phrase_guessed(letter, running):
    phrase_start = letter.find(' ') + 1
    phrase = letter[phrase_start:]

    if phrase.title() == chosen.title(): print('\nCongratulations, you guessed correctly!')
    else: print('\nGame Over. You guessed incorrectly.')


def winning_letter(letter, running, phrase_blanks):
    phrase_no_blanks = ''.join(phrase_blanks)
    chosen_no_blanks = chosen.title().replace(" ", "").lower()

    if phrase_no_blanks == chosen_no_blanks:
        print('\nCongratulations, you won!')
        return True

    return False



if __name__ == '__main__':

    running = True
    
    while True:
        correct = list()
        incorrect = list()
        misses = 0
        display_win = False
        
        chosen = random.choice(list(open("Phrases.txt"))).strip()
        blanks_format, spaces = create_blanks(chosen)
        enter = game_rules()

        while enter.strip() != '':
            enter = input('\nPress enter to start the game\n')

        print_blanks(blanks_format, spaces)

        
        while running:
            letter = input('\n\nChoose a letter: ')

            if letter.strip()[:5].lower() == 'guess':
                check_phrase_guessed(letter, running)
                break

            elif len(letter.strip()) != 1:
                print('Input must be one character.')
                continue

            elif letter.isalpha():
                if letter.lower() in correct:
                    print(f'"{letter}" has already been used.')
                    continue
                
                elif letter.lower() in chosen or letter.upper() in chosen:
                    correct.append(letter.lower())
                    print(f'"{letter}" is in the phrase.')

                    image = update_image(misses)                    
                    display_image(image)

                    blanks_format = update_blanks(blanks_format, chosen.lower(), letter)
                    print_blanks(blanks_format, spaces)
                    print('-' * 52)

                    if winning_letter(letter, running, blanks_format):
                        break
                    
                elif letter.lower() not in chosen and letter.lower() not in incorrect:
                    print(f'"{letter}" is NOT in the phrase.')
                    incorrect.append(letter.lower())

                    misses += 1
                    image = update_image(misses)

                    if image == "Game Over":
                        break
                    
                    display_image(image)
                    print_blanks(blanks_format, spaces)
                    print('-' * 52)

                else:
                    print(f'"{letter}" is not in the phrase and it has already been used.')

            else:
                print('Input must be a letter.')
                continue


            if '_' not in blanks_format:
                running = False

        
        restart = input('Would you like to restart the game? (Yes/No)\n')
        if restart.lower() == 'no': quit()
        else:
            running = True
