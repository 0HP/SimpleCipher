import RSA
import AES
import TEA

def __main__():
    SelectFunc = "Please select the functions\n"
    SelectEncrypt = "0: Encrypt\n"
    SelectDecrypt = "1: Decrypt\n"
    SelectSign = "2: Signature\n"
    SelectAuth = "3: Authentication\n"
    SelectOut = "Other: Exit\n"

    while True:
        Project = input(SelectFunc+SelectEncrypt+SelectDecrypt+SelectSign+SelectAuth+SelectOut)

        #Encrypt
        if Project == "0":
            SelectAlgo = input("Please select the encrypt algorithm\n"+"0: AES(CRT)\n"+"1: TEA(CRT/CBC)\n"+"Other : RSA(2048bits)\n")

            #AES
            if SelectAlgo == "0":
                AESOJ = AES.AES()

                KeyFile = input("Please input the key file(file path)\n")
                AESOJ.GetKey(KeyFile)
                AESOJ.ExpanKey()

                CounterFile = input("Please input the counter file(file path)\n")
                AESOJ.GetCounter(CounterFile)

                PlainFile = input("Please input the file ready to encrypt\n")
                AESOJ.GetPlain(PlainFile)
                AESOJ.Padding()
                AESOJ.BlockMessage()

                CipherFile = input("Please input the file to save the ciphertext\n")
                if AESOJ.Encrypt(CipherFile):
                    print("Encrypt Successful!\n")
                else:
                    print("Encrypt Fail\n")
                    exit(1)

            #TEA
            elif SelectAlgo == "1":
                TEAOJ = TEA.TEA()
                Moduel = input("Please select the encrypt moduel\n"+"0: CRT\n"+"1: CBC\n")
                TEAOJ.SelectModule(Moduel)

                TEAKey = input("Please input the key file(file path)\n")
                TEAOJ.ReadKey(TEAKey)

                PlainFile = input("Please input the file ready to encrypt\n")
                TEAOJ.ReadFile(PlainFile)

                CipherFile = input("Please input the file to save the ciphertext\n")

                if Moduel=="0":
                    CounterFile = input("please input the initial counter file\n")
                    TEAOJ.ReadCount(CounterFile)
                    if TEAOJ.TEACryptCounter(CipherFile):
                        print("Encrypt Successful!\n")
                    else:
                        print("Encrypt Fail\n")
                        exit(1)

                elif Moduel=="1":
                    CBCVIFile = input("Please input the initial CBC VI file\n")
                    TEAOJ.ReadVI(CBCVIFile)
                    if TEAOJ.TEACryptCBC(CipherFile):
                        print("Encrypt Successful!\n")
                    else:
                        print("Encrypt Fail\n")
                        exit(1)
                else:
                    exit(1)

            #RSA
            else:
                RSAOJ=RSA.RSA()
                Pukey = input("Please input the public key(file path)\n")
                RSAOJ.GetPrKey(Pukey)

                PlainFile = input("Please input the file ready to encrypt\n")
                RSAOJ.GetPlain(PlainFile)
                RSAOJ.BlockMessage(128)

                CipherFile = input("Please input the file to save the ciphertext\n")
                if RSAOJ.Encrypt(CipherFile):
                    print("Encrypt Successful!\n")
                else:
                    print("Encrypt Fail\n")
                    exit(1)

            continue
        #Decrypt
        elif Project == "1":
            SelectAlgo = input("Please select the decrypt algorithm\n" + "0: AES(CRT)\n" + "1: TEA(CRT/CBC)\n" + "Other : RSA(2048bits)\n")

            # AES
            if SelectAlgo == "0":
                AESOJ = AES.AES()

                KeyFile = input("Please input the key file(file path)\n")
                AESOJ.GetKey(KeyFile)
                AESOJ.ExpanKey()

                CounterFile = input("Please input the counter file(file path)\n")
                AESOJ.GetCounter(CounterFile)

                CipherFile = input("Please input the file ready to decrypt\n")
                AESOJ.GetPlain(CipherFile)
                AESOJ.BlockMessage()

                PlainFile = input("Please input the file to save the plaintext\n")
                if AESOJ.Encrypt(PlainFile):
                    print("Decrypt Successful!\n")
                else:
                    print("Decrypt Fail\n")
                    exit(1)

            # TEA
            elif SelectAlgo == "1":
                TEAOJ = TEA.TEA()
                Moduel = input("Please select the decrypt moduel\n" + "0: CRT\n" + "1: CBC\n")
                TEAOJ.SelectModule(Moduel)

                TEAKey = input("Please input the key file(file path)\n")
                TEAOJ.ReadKey(TEAKey)

                CipherFile = input("Please input the file ready to decrypt\n")
                TEAOJ.ReadFile(CipherFile)

                PlainFile = input("Please input the file to save the plaintext\n")

                if Moduel == "0":
                    CounterFile = input("please input the initial counter file\n")
                    TEAOJ.ReadCount(CounterFile)
                    if TEAOJ.TEADecryCounter(PlainFile):
                        print("Decrypt Successful!\n")
                    else:
                        print("Decrypt Fail\n")
                        exit(1)

                elif Moduel == "1":
                    CBCVIFile = input("Please input the initial CBC VI file\n")
                    TEAOJ.ReadVI(CBCVIFile)
                    if TEAOJ.TEADecryCBC(PlainFile):
                        print("Decrypt Successful!\n")
                    else:
                        print("Decrypt Fail\n")
                        exit(1)
                else:
                    exit(1)

            # RSA
            else:
                RSAOJ = RSA.RSA()
                Prkey = input("Please input the private key(file path)\n")
                RSAOJ.GetPuKey(Prkey)

                CipherFile = input("Please input the file ready to decrypt\n")
                RSAOJ.GetPlain(CipherFile)
                RSAOJ.BlockMessage(256)

                PlainFile = input("Please input the file to save the plaintext\n")
                if RSAOJ.Decrypt(PlainFile):
                    print("Decrypt Successful!\n")
                else:
                    print("Encrypt Fail\n")
                    exit(1)

            continue
        #Signatrue
        elif Project == "2":
            RSAOJ=RSA()
            Prkey = input("Please input the private key(file path)\n")
            RSAOJ.GetPrKey(Prkey)

            PlainFile = input("Please input the file ready to Signature\n")
            SaveFile = input("Please input the file to save the Signatrue\n")

            if RSAOJ.SignNature(PlainFile,SaveFile):
                print("Signatrue Successful!\n")
            else:
                print("Signatrue Fail!\n")
                exit(1)
            continue
        #Authentication
        elif Project == "3":
            RSAOJ = RSA()
            Pukey = input("Please input the public key(file path)\n")
            RSAOJ.GetPuKey(Prkey)

            SignFile = input("Please input the Signature File\n")
            MessageFile = input("Please input the Message file\n")

            if RSAOJ.Auth(SignFile,MessageFile):
                print("Authentication Successfully!\n")
            else:
                print("Authentication Fail!\n")
                exit(1)
            continue
        #exit
        else:
            break

if __name__=="__main__":
    __main__()