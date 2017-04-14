from pyfiglet import Figlet
from functions import *

if __name__ == '__main__':

    # cool boi
    #
    # f = Figlet(font='slant')
    # print(f.renderText("CCVS"))
    # print("CaesarCypherVideoSteganography")
    # print("")
    # print("By : ")
    # print("")
    # print("===Fauzanil Zaki===")
    # print("====Galih Dea P.===")
    # print("====Johan Eko P.===")
    # print("===Wiladhianty Y.==")
    #


    file_name = raw_input("Filename ? : ")
    img = Image.open("temp/"+file_name)
    print(img,img.mode)

    secret_msg = ""

    secret_msg_open = open("data/text-to-hide.txt","r")
    for line in secret_msg_open:
        secret_msg += line

    print(secret_msg)

    frame_encoded = encode_frame(img,secret_msg)

    if frame_encoded:
        frame_encoded.save("data/enc-"+file_name)

    #decode

    secret_msg_open = open("data/text-to-hide.txt","w")
    secret_msg_open.write("")

    img = Image.open("data/enc-"+file_name)
    hidden_text = decode_frame(img)
    text = open("data/recovered-text.txt","w")
    text.write(hidden_text)

