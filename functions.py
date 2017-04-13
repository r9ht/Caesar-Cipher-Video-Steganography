from PIL import Image

# references :
#
# https://www.daniweb.com/programming/software-development/code/485063/hide-private-message-in-an-image-python
# http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/

def encode_frame(frame,msg):

    # using the red channel to hide ASCII values

    length = len(msg)

    # limit text to 255 for each frame

    if length > 255:
        print("text too long! (don't exeed 255 characters)")
        return False
    if frame.mode != 'RGB' :
        print("Image must be in RGB format")
        return False

    # use a copy of image to hide the text in

    encoded = frame.copy()
    width,height = frame.size
    index = 0
    for row in range(height):
        for col in range(width):
            r,g,b = frame.getpixel((col,row))

            # first value is length of the message per frame
            if row == 0 and col == 0 and index < length:
                asc = length
            elif index <= length:
                c = msg[index -1]
                asc = ord(c)
            else:
                asc = r
            encoded.putpixel((col,row),(asc,g,b))
            index += 1
    return encoded


def decode_frame(frame):

    width,height = frame.size
    msg = ""
    index = 0
    for row in range(height):
        for col in range(width):
            try:
                r,g,b = frame.getpixel((col,row))
            except ValueError:
                # for some png a(transparency) is needed
                r,g,b,a = frame.getpixel((col,row))
            # first pixel is the information about length of the message
            if row == 0 and col == 0:
                length = r
            elif index <= length:
                msg += chr(r)
            index += 1
    return msg





