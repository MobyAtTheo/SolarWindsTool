#!/usr/bin/env python3

import base64
import getpass


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
        pass
 
    def encodePW(self):
        print("encodePW")
        myPassword = ""

        myUserName=input("Username: ")
        myPassWord=getpass.getpass("Password: ")

        myPassWord.strip()
        print(myPassWord)
        b64PassWord=base64.b64encode(myPassWord.encode('ascii'))
        print(b64PassWord)

        return str(b64PassWord)

    def decodePW(self,b64Password):
        print(b64Password)
        decodedPW=base64.b64decode(b64Password.encode('ascii'))
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
    myPassword=genBase64Pass.encodePW("test")
    print("mypasshere: ",myPassword)
    genBase64Pass.outputPW("blah",myPassword,"defaultuser")
    
    myDecodedPW=genBase64Pass.decodePW("blah",myPassword)
    genBase64Pass.outputPW("blah",myDecodedPW,"defaultuser")




