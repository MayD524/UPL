import string
import random
class cipher:

    def genKey(maxCount = 10):
        endStr = ""
        for i in range(maxCount):
            tmp = string.printable.strip()
            endStr += ''.join(random.sample(tmp, len(tmp)))

        return endStr
    
    def decryptString(key, ctext):
        plaintext = ""
        for i in range(len(ctext)):
            ctextChar = ord(ctext[i])
            keyChar = ord(key[i])
            plaintext += chr(ctextChar - keyChar)
        
        return plaintext

    def encryptString(key, plaintext):
        endStr = ""
        for i in range(len(plaintext)):
            plainChar = ord(plaintext[i])
            keyChar = ord(key[i])
            endStr += chr(plainChar + keyChar)

        return endStr

