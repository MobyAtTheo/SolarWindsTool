#!/usr/bin/env python

import base64
import getpass


class genBase64Pass(object):
    """Generate an encoded password for use in stored files.
    """

    """Future: use encrypt / decrypt or keys model"""

    """
        >>> base64.b64encode("test".encode('ascii'))
        b'dGVzdA=='
        >>> base64.b64decode("dGVzdA==".encode('ascii'))
        b'test'
    """

    def __init__(self):
        #self.myPassword
        self.myUserName="username123"
        self.myPassWord="password123"
        #pass
 
    def getDataPW(self):
        #print("encodePW")
        """future: extend to get username and write the files for the creds"""
        myPassword = ""

        #self.myUserName=raw_input("Username: ")
        self.myPassWord=getpass.getpass("Password: ")

        self.myPassWord.strip()
        self.myUserName.strip()

        return self.myPassWord

    def encodePW(self,myPassWord):
        b64PassWord=base64.b64encode(myPassWord)

        return b64PassWord

    def decodePW(self,b64Password):
        #decodedPW=base64.b64decode(b64Password.encode('ascii'))
        decodedPW=base64.b64decode(b64Password)

        return str(decodedPW)

    def outputPW(self,outputPW,outputUser,encodedPW):
        """ May be needed in python3 to strip leading characters from
            base64 module off of unicode ouput string
        """
        print "*********************"
        print "[+] User:"
        print outputUser.strip()
        print "[+] Encoded Password: "
        print encodedPW

if __name__ == '__main__':
    #print("main")
    genPass=genBase64Pass()
    plaintextPW=genPass.getDataPW()

    """uncomment next 2 lines if you'd like to see the password you entered for code sanity check"""
    ### print"[+] Password to be encoded: "
    ### print plaintextPW

    myPassword=genPass.encodePW(plaintextPW)
    print "[+] Encoded Password: "
    print myPassword

    myDecodedPW=genPass.decodePW(myPassword)
    """uncomment next 2 lines if you'd like to see your password decoded for code sanity check"""
    ### print "[+] Decoded Password: "
    ### print myDecodedPW

    """Activate after enabling user password for debugging"""
    #genPass.outputPW(myDecodedPW,"defaultuser",myPassword)




