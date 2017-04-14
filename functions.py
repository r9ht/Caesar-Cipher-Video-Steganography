from PIL import Image
import shutil,cv2,os

# references :
#
# https://www.daniweb.com/programming/software-development/code/485063/hide-private-message-in-an-image-python
# http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
# http://tsaith.github.io/combine-images-into-a-video-with-python-3-and-opencv-3.html


def frame_extract(video):
    temp_folder = 'temp'
    try:
        os.mkdir(temp_folder)
    except OSError:
        remove(temp_folder)
        os.mkdir(temp_folder)

    vidcap = cv2.VideoCapture("data/"+str(video))
    count = 0

    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.jpg".format(count)), image)
        count += 1

def frame_merge(dir_path,img_ext,output_name):
    images = []
    frame_count = len(os.listdir(dir_path))

    for i in range(frame_count):
        images.append(str(i)+".jpg")

    sample_image = os.path.join(dir_path,images[0])
    sample_frame = cv2.imread(sample_image)
    height,width,channels = sample_frame.shape

    fourcc = cv2.cv.CV_FOURCC(*'MP4V')
    out = cv2.VideoWriter(output_name, fourcc, 30.0, (width, height))
    images.sort()
    for i in range(frame_count):
        image_path = os.path.join(dir_path,str(i)+".jpg")
        frame = cv2.imread(image_path)
        out.write(frame)
        cv2.imshow('video',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):  # Hit `q` to exit
            break

    out.release()
    cv2.destroyAllWindows()

    print("The output video is {}".format(output_name))


def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))




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





