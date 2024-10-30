import argparse
import re
import os
import sys
def count_word_in_file(file_name, word):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            total_word_count = text.lower().split().count(word.lower())
            direcitves = re.findall(r'\\input\{([^}]*)}', text)

            for input_file in direcitves:
                pid = os.fork()
                if pid == 0:
                    word_count = count_word_in_file(input_file, word)
                    sys.exit(word_count)
            
            for _ in direcitves: # idziemy w dół i na samym końcu tylko czekamy
                if pid != 0:
                    status = os.wait()
                    word_count = os.WEXITSTATUS(status[1]) # Odczytuje kod wyjścia z zakończonego procesu
                    total_word_count += word_count
                
            return total_word_count
    except FileNotFoundError:
        print(f"Plik '{file_name}' nie został znaleziony.")
        return 0




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Zlicz wystąpienia słowa w pliku tekstowym.')
    parser.add_argument('-p', '--plik', required=True, help='Nazwa pliku z tekstem')
    parser.add_argument('-s', '--slowo', required=True, help='Słowo do zliczenia')

    args = parser.parse_args()

    count = count_word_in_file(args.plik, args.slowo)
    print(f"Słowo '{args.slowo}' występuje {count} razy w pliku '{args.plik}'.")
