import cv2, os, numpy

def contrast_limited_adaptive_HE(channel_img):
    assert(len(channel_img.shape)==2)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))      # Create CLAHE Object
    clahe_image = numpy.empty(channel_img.shape, dtype='uint8')
    clahe_image = clahe.apply(numpy.array(channel_img, dtype='uint8'))

    return clahe_image

def image_preprocessing(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(img)
    l = contrast_limited_adaptive_HE(l)

    processed_image = cv2.merge((l, a, b))
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_LAB2RGB)
    
    return processed_image

def preprocess(fname):
    images = []

    Mask = numpy.zeros((600, 600), dtype='uint8')
    Mask[Mask.shape[0]//2][Mask.shape[1]//2] = 255
    GLCMask = cv2.dilate(Mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                        (Mask.shape[0]-30, Mask.shape[1]-30)), iterations=1)
    _img = cv2.imread(fname)
    _img = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
    _img = cv2.resize(_img, (600, 600))
    _img = cv2.bitwise_and(_img, _img, mask=GLCMask)
    _img = cv2.resize(_img, (384, 384))
    _img = image_preprocessing(_img)

    images.append(_img)
    images = numpy.array(images, dtype='uint8')
    return images
