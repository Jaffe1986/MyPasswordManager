from duplicateRemover import DuplicateRemover

class Decryptor:

    def __init__(self, passcode, message):
        # create untouchable alphabet
        self.alphabetPrime = self.alphabetPrime = [chr(i) for i in range(32, 127) if chr(i) not in {"'", '"', '{', '}'}]
        self.message = message  # Store message to be encrypted
        self.filteredSecret = DuplicateRemover(passcode)  # Fileter passcode for duped characters
        self.shiftedAlphabet = []  # Create list to store secret character

        for char in self.filteredSecret.result:  # Add each character of filterSecret to shiftedAlphabet
            self.shiftedAlphabet.append(char)

        for char in self.alphabetPrime:  # Add any remaining character that is not in filtered secert from aplphabetPrime into shiftedAlphabet
            if char not in self.filteredSecret.result:
                self.shiftedAlphabet.append(char)

        self.unsecretMessage = ''  # Create string to store encrypted message

        for char in self.message:  # Ecrypt message
            i = 0  # index counter
            for letter in self.shiftedAlphabet:  # check index of char for index location in alpabet prime
                if char != letter:
                    i += 1
                elif char == letter:
                    self.unsecretMessage += self.alphabetPrime[i]
                    break