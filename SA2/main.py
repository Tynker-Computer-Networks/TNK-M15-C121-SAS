import zipfile
import itertools
import string


def is_zip_encrypted(zipFilePath):
    try:
        with zipfile.ZipFile(zipFilePath, 'r') as zip_file:
            for zip_info in zip_file.infolist():
                if zip_info.flag_bits & 0x1:
                    return True
            return False
    except zipfile.BadZipFile:
        return False


def main():
    folderpath = input('Path to the file: ')
    folderpath = folderpath.strip()
    # Get the expected password length from the user
    passwordLength = int(
        input("Up to which length you wan to check the password: "))

    if (not is_zip_encrypted(folderpath)):
        print('The zipped file/folder is not password protected! You can successfully open it!')
    else:
        result = 0
        print("Brute Force Started...")

        if (result == 0):
            print(
                f"Checking for up to {passwordLength} characters long passwords...")
            # Get the all characters form string library
            chars = string.printable.strip()
            attempts = 0
            # Run the loop up to the length of the password the user is looking for...
            for length in range(1, passwordLength + 1):
                # Notifies for how much length of password currently programming is checking
                print(f"Checking for length {length}.")
                for guess in itertools.product(chars, repeat=length):
                    attempts += 1
                    guess = ''.join(guess)
                    try:
                        with zipfile.ZipFile(folderpath, 'r') as zf:
                            guess = guess.encode('utf8').strip()
                            zf.extractall(pwd=guess)
                            guess = guess.decode('utf8').strip()
                            result = 1
                            break
                    except:
                        pass

                if (result == 1):
                    break

        if (result == 0):
            message = f"Sorry, password not found. A total of {attempts} possible combinations tried. Password is not of {passwordLength} characters."
            print(message)

        else:
            message = f"Congratulations!!! Password found after trying {attempts} combinations.\nThe password is {str(guess)}."
            print(message)

main()
