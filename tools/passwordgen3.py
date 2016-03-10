#!/usr/bin/env python3

import base64
import getpass

"""note this code is WIP"""
class genBase64Pass(object):
    """
    """

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
        myPassword = ""

        self.myUserName=input("Username: ")
        self.myPassWord=getpass.getpass("Password: ")

        self.myPassWord.strip()
        self.myUserName.strip()

        return str(self.myPassWord)

    def encodePW(self,myPassWord):
        #print(self.myPassWord)
        print(myPassWord)
        #b64PassWord=base64.b64encode(self.myPassWord.encode('ascii'))
        #print(b64PassWord)

        #return str(b64PassWord)

    def decodePW(self,b64Password):
        print("b64Passwordencoded: ")
        print(b64Password)
        #decodedPW=base64.b64decode(b64Password.encode('ascii'))
        decodedPW=base64.b64decode(b64Password)
        print("decodedPW: ")
        print(decodedPW)

        return str(decodedPW)

    def outputPW(self,outputPW,outputUser):
        print("Password: ")
        print(outputPW)
        print("User:")
        print(outputUser)

if __name__ == '__main__':
    print("main")
    genPass=genBase64Pass()
    plaintextPW=genPass.getDataPW()
    myPassword=genBase64Pass.encodePW("test",str(plaintextPW.encode('ascii')))
    print("mypasshere: ",myPassword)
    genBase64Pass.outputPW("blah",myPassword,"defaultuser")
    
    myDecodedPW=genBase64Pass.decodePW("blah",myPassword)
    genBase64Pass.outputPW("blah",myDecodedPW,"defaultuser")




