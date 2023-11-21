# Library used for password encrypted zipped folder/file
import zipfile


# This is the helper function
def is_zip_encrypted(zipFilePath):
    try:
        with zipfile.ZipFile(zipFilePath, 'r') as zip_file:
            # Retrieve the encryption information for each file in the zip
            for zip_info in zip_file.infolist():
                if zip_info.flag_bits & 0x1:
                    return True
            return False
    except zipfile.BadZipFile:
        # If the file is not a valid zip file
        return False


def main():
    # Get the target file path from the user
    folderpath = input('Path to the file: ')
    folderpath = folderpath.strip()

    # Checks if the file is password encrypted
    if (not is_zip_encrypted(folderpath)):
        # Notifies if the zipped file/folder is not password encrypted
        print('The zipped file/folder is not password protected! You can successfully open it!')

    else:
        result = 0  # Intialize a variable result with zero. '0' will indicate Failure, while '1' will idicate Success
        attempts = 0  # Initialize a variable attempts to keep the count of passwords tried

        # Build a character array including all numbers,lowercase letter, uppercase letters and special haracters. Total 10+26+26+33 = 95 characters
        characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'k', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                      'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'p', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                      '!', '@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')', '<', '}', '{', '^', '[', ']', ' ', '+', '-', '_', '&', ';', '"', '?', '`', "'", '\\']

        print("Brute Force Started...")

        # If still the password is not found i.e. result = 0, the below loop will try four character passwords. 81450625 Possible Combinations
        if (result == 0):
            print("Checking for 4 character password...")
            for i in characters:
                for j in characters:
                    for k in characters:
                        for l in characters:
                            guess = str(i) + str(j) + str(k) + str(l)
                            guess = guess.encode('utf8').strip()
                            attempts += 1
                            try:
                                with zipfile.ZipFile(folderpath, 'r') as zf:
                                    zf.extractall(pwd=guess)
                                    # Decoding the guess string
                                    guess = guess.decode('utf8').strip()
                                    result = 1  # Set result variable to 1 on success
                                    break  # If the password is found break from i for loop
                            except:
                                pass
                        if result == 1:
                            break  # If the password is found break from j for loop
                    if result == 1:
                        break  # If the password is found break from k for loop
                if result == 1:
                    break  # If the password is found break from l for loop

        # Finally, if the password is not found even after appying all possile combination of characters upto 4 character length, notify the user as below, else print congratulations
        if (result == 0):
            message = f"Sorry, password not found. A total of {attempts} possible combinations tried. Password is not of 4 characters."
            print(message)

        else:
            message = f"Congratulations!!! Password found after trying {attempts} combinations.\nThe password is {guess}."
            print(message)


main()
