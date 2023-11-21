# -------------------
# Install PyPDF2 library using below command
# pip3 install 'PyPDF2<3.0'

# Dictionary Attack
# --------------------

import PyPDF2 as pd


def main():
    # Get the target file path from the user
    filename = input('Path to the file: ')
    filename = filename.strip()
    # Read the PDF file as binary object
    file = open(filename, 'rb')
    pdfReader = pd.PdfFileReader(file)

    attempts = 0

    # Checks if the file is password encrypted
    if not pdfReader.isEncrypted:
        print('The file is not password protected! You can successfully open it!')
    else:
        # Reading the wordlist to perfrom Dictionary attack
        wordListFile = open('wordlist.txt', 'r', errors='ignore')
        body = wordListFile.read().lower()
        words = body.split('\n')

        for i in range(len(words)):
            word = words[i]
            print(f'Trying to decode passowrd by: {word}')
            result = pdfReader.decrypt(word)
            if result == 1:
                print(f"Congratulations!!! The password is {word}.")
                break

            elif result == 0:
                attempts += 1
                print(f'Passwords attempts: {str(attempts)}')
                continue


main()
