from PIL import Image
import numpy as np

noOfDivs = 15

def convertImg(file):
    """
    Converts image file to numpy data values (pixel values).
    
    file: filename with path and extension
    
    return: pixel data values
    """
    
    # Gets pixel values
    im = Image.open(file)
    pixels = list(im.getdata())
    width, height = im.size
    
    # Convert RGB values (R, G, B, x to '0' for 'white' & '1' for 'black'
    pixels=[int(i[0]/255) for i in pixels]
    
    # Convert 1-D list of values to 2-D list
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    
    # List -> Numpy array
    data = np.array(pixels)
    
    return data

def printOrigImg(data):
    '''
    Prints the image on the terminal.
    
    data: pixel data of image (from 'convertImg()')
    
    return: NULL
    '''
    
    for i in range(256):
        for j in range(256):
            print(data[i][j], end="")
        print()
        
def printCroppedImg(dataCropped, top, bottom, left, right):
    '''
    Prints the cropped image on the terminal .
    
    dataCropped: cropped pixel data of image (from 'crop()')
    top: top-most index bound of image
    bottom: bottom-most index bound of image
    left: left-most index bound of image
    right: right-most index bound of image
    
    return: NULL
    '''
    
    for i in range(bottom-top):
        for j in range(right-left):
            print(dataCropped[i][j], end="")
        print()
    
def crop(data):
    '''
    Crops the pixel values into a tight image.
    
    data: pixel data of image (from 'convertImg()').
    
    return: 
        dataCropped: cropped pixel data
        top: top-most index bound of image
        bottom: bottom-most index bound of image
        left: left-most index bound of image
        right: right-most index bound of image
    '''
    
    # Lower bound
    for i in range(256):
        for j in range(256):
            if data[i][j] == 0:
                bottom = i - 1
                break
    
    # Upper bound
    top = np.argwhere(data == 0)
    top = top[0][0] + 1
            
    # Transpose to find right & left bound
    dataTrans = data.T
        
    # Right bound
    for i in range(256):
        for j in range(256):
            if dataTrans[i][j] == 0:
                right = i + 1
                break

    # Left bound
    left = np.argwhere(dataTrans == 0)
    left = left[0][0] - 1
    
    # Adjust / Fine-tune bound values
    top-=1
    bottom+=2
    left+= 1
    
    # Height & width (if required)
    height = bottom-top
    width = right-left
    
    divs = noOfDivs
    
    # Adjust height
    heightBuffer = divs - ((height) % divs)
    top -= heightBuffer // 2
    bottom += heightBuffer - heightBuffer // 2
    
    # Adjust width
    widthBuffer = divs - ((width) % divs)
    left -= widthBuffer // 2
    right += widthBuffer - widthBuffer // 2
    
    # The crop part. It slices the list
    dataCropped = []
    
    for i in range(top,bottom):
        dataCropped += [data[i][left:right]]
        
    return dataCropped, top, bottom, left, right
    
def segment(dataCropped, top, bottom, left, right):
    '''
    Segments the dataCropped into a 'divs x divs' matrix of ratio of number of black pixels to white pixels in that segment
    
    dataCropped: The cropped pixel data of image (from 'crop()')
    top: top-most index bound of image
    bottom: bottom-most index bound of image
    left: left-most index bound of image
    right: right-most index bound of image
    
    return: 'divs x divs' matrix of ratio of blacks : total
    '''

    divs = noOfDivs
    global FINISHED

    # Segments the pixel data into 'divs x divs'
    height = bottom - top
    width = right - left
    heightseg = height // divs
    widthseg = width // divs
    
    values = []
    count = 0
    
    for i in range(divs):
        values += [[]]
        for j in range(divs):
            values[i] += [0]
            count = 0
            for k in range(i * heightseg, i * heightseg + heightseg):
                for l in range(j * widthseg, j * widthseg + widthseg):
                    if dataCropped[k][l] == 0:
                        count += 1
    
            if (heightseg * widthseg == count):  
                values[i][j] = 1.0
            else:
                values[i][j] = count / ((heightseg * widthseg) - count)

    values = np.array(values)
    
    return values

trained_data = {}

for i in range(10):
    # File number
    num = i
    for j in range(1, 9):
        # Change directory before use
        file = '/Users/sheriffabdullah/Coding/Project/Number Recognition/Number Samples/%d/%d_%d.png' % (i,i,j)
        #file = '/Users/sheriffabdullah/Coding/Project/Number Recognition/test2.png'
        dataCropped, top, bottom, left, right = crop(convertImg(file))
        trained_data[str(i)+'_'+str(j)] = segment(dataCropped,top,bottom,left,right)
        

