import cv2
import base64
import numpy as np

# class that builds an image from a blob
class ImageHandler: 

    isFirstImageCaptured = False

    showRawCapture = True

    #shi-tomasi corner detector parameters

    feature_params = dict( maxCorners = 100, qualityLevel = 0.3, minDistance = 7, blockSize = 7 )

    #lucas kanade optical flow parameters

    lk_params = dict( winSize  = (15,15), maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    '''
    def __init__(self):
        #initializes blank image
        self.previousImage = np.zeros((320, 240), np.uint8) 
    '''

    def handleImageBlob(self, blob):
        processedImage = self.convertFromBlob(blob)

        if self.isFirstImageCaptured == True: 
            self.calculateOpticalFlow(self.previousImage, processedImage)
        self.previousImage = processedImage
        self.isFirstImageCaptured = True

    #converts blob sent from esp32 into image
    def convertFromBlob(self, blob):
        nparr = np.frombuffer(blob, np.uint8)
        img = cv2.imdecode(nparr, flags=cv2.IMREAD_GRAYSCALE)

 

        return img

    def calculateOpticalFlow(self, previousImage, currentImage):

        color = np.random.randint(0,255,(100,3))

        mask = np.zeros_like(previousImage)

        p0 = cv2.goodFeaturesToTrack(previousImage, mask = None, **self.feature_params)
        
        p1, st, err = cv2.calcOpticalFlowPyrLK(previousImage, currentImage, p0, None, **self.lk_params)

        good_new = p1[st==1]

        good_old = p0[st==1]

            # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
            currentImage = cv2.circle(currentImage,(a,b),5,color[i].tolist(),-1)
        img = cv2.add(currentImage,mask)

        cv2.imshow('currentImage',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            cap.release()



