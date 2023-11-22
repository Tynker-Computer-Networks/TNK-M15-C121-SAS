import zipfile
import itertools
import string
import time
import PyPDF2 as pd


def is_zip_encrypted(zipFilePath):
    try:
        with zipfile.ZipFile(zipFilePath, 'r') as zip_file:
            for zip_info in zip_file.infolist():
                if zip_info.flag_bits & 0x1:
                    return True
            return False
    except zipfile.BadZipFile:
        return False


def is_pdf_encrypted(pdfFilePath):
    try:
        file = open(pdfFilePath, 'rb')
        pdfReader = pd.PdfFileReader(file)
        return pdfReader.isEncrypted
    except Exception as e:
        return False


def main():
    # Get the target file type from the user
    fileType = input(
        "Select the filetype:\n1.ZIP\n2.PDF\nEnter the Selection: ")
    folderpath = input('Path to the file: ')
    folderpath = folderpath.strip()
    passwordLength = int(
        input("Up to which length you wan to check the password: "))

    # Add elif block to check is PDF file is encrypted or not
    if (not is_zip_encrypted(folderpath) and fileType == "1"):
        print('The zipped file/folder is not password protected! You can successfully open it!')
    elif (not is_pdf_encrypted(folderpath) and fileType == "2"):
        print(
            'The PDF file/folder is not password protected! You can successfully open it!')
    else:
        result = 0
        print("Brute Force Started...")
        starttime = time.time()

        if (result == 0):
            print(
                f"Checking for up to {passwordLength} characters long passwords...")

            chars = string.printable.strip()
            attempts = 0

            for length in range(1, passwordLength + 1):
                print(f"Checking for length {length}.")
                for guess in itertools.product(chars, repeat=length):
                    attempts += 1
                    guess = ''.join(guess)

                    # Write condition to handle zip files filetype.
                    if (fileType == "1"):
                        try:
                            with zipfile.ZipFile(folderpath, 'r') as zf:
                                guess = guess.encode('utf8').strip()
                                zf.extractall(pwd=guess)
                                guess = guess.decode('utf8').strip()
                                result = 1
                                endtime = time.time()
                                break
                        except:
                            pass

                    # Write condition to handle pdf files filetype.
                    if (fileType == "2"):
                        try:
                            file = open(folderpath, 'rb')
                            pdfReader = pd.PdfFileReader(file)
                            passwordChecker = pdfReader.decrypt(guess)
                            if (int(passwordChecker) == 1):
                                result = 1
                                endtime = time.time()
                                break
                        except:
                            pass

                if (result == 1):
                    break

        duration = starttime + endtime
        if (result == 0):
            message = f"Sorry, password not found. A total of {attempts} possible combinations tried in {duration} seconds. Password is not of {passwordLength} characters."
            print(message)

        else:
            message = f"Congratulations!!! Password found after trying {attempts} combinations tried in {duration} seconds.\nThe password is {str(guess)}."
            print(message)


main()
