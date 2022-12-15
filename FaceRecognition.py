import numpy as np
import cv2 
import tkinter as tk
import threading
import functools
from PIL import Image, ImageTk

class FaceDetector(object):        
    
    FACE_DETECTOR_PATH = "C:/Users/JohnC/Anaconda3/envs/opencv2/Library/etc/haarcascades/haarcascade_frontalface_default.xml"

    window = None
    panel = None
    frame = None
    capture = None

    hog = None            
    data = []

    running = False


    def GetData(self):
        try:
            res = [self.frame, max(self.data)]
            self.data = []
            return res
        except:
            pass
        return []        

    def GetFaceData(self):
        ret, self.frame = self.capture.read()
    
        face_detector = cv2.CascadeClassifier(self.FACE_DETECTOR_PATH)
        rects = face_detector.detectMultiScale(self.frame)
        rects = [Rect(r) for r in rects]

        #print(*[F"[{i}]: {rects[i]}" for i in range(len(rects))], sep=' | ')

        return rects      
   
    


    def Execute(self):        
        cv2.startWindowThread()
        self.capture = cv2.VideoCapture(0)
        self.data = []
        self.running = True

        A = []

        while self.running:
            ret, self.frame = self.capture.read()
            self.frame = cv2.resize(self.frame, (640, 480))
            
            self.data = self.GetFaceData()            


    def __init__(self, win):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        self.window = win
        #self.panel = tk.Label(win)
        #self.panel.pack()
        #self.panel.grid(row = 0, column = 0)        

"""==============================================================="""

class FaceData(object):

    rects = []    

    vert_mean = 0    
    size_mean = 0
    vert_var = 0
    size_var = 0

    def __init__(self):        
        pass


    # Apply low-variance filter to remove non-faces (e.g., oval-shaped objects around the room, pictures of people in the background, etc.)

    def Filter(rects):
        """     
        Notes:        

        Values of stationary objects that return false positives often deviate by a 1-3 pixels between captures (why?). Temporary approach for resolving
        these discrepancies will be to calculate overlapping area of previously found rectangles and compare it to a threshold percentage. Look for 
        potentially faster alternatives
        _________________________________________________________________________        

        TODO: Find approach for filtering out legitimate facial matches as well (e.g., coworkers who sit nearby and will 
        always remain in frame). These can probably be deduced easily based on proximity to center of frame (Euclidean),
        but in special cases perhaps a user-defined minimum threshold for valid rectangle sizes would suffice to get the
        rest. [Attempted solution with "Missing Value Ratio" technique, but warrants further testing]

        TEST: Consider in what cases (if any) could a matching rectangle be found that may be *larger* than the correct one (that would not 
        already be filtered out due to low variance)?                

        """

        # Normalize value into 0-1 range
        def Normalize(val, min, max):
            return (val - min) / ((max - min) if max != min else max)
        

        # Calculates number of overlapping pixels between two rectangles
        def OverlappingArea(a, b):
            a, b = sorted([a, b])

            if b.y0 > a.y1 or b.x0 > a.x1: 
                return 0
            
            area = (a.Area() + b.Area())

            x_dist = min(a.x1, b.x1) - max(a.x0, b.x0)
            y_dist = min(a.y1, b.y1) - max(a.y0, b.y0)

            intersection = (x_dist * y_dist) if (x_dist > 0 and y_dist > 0) else 0
       
            return area - intersection

        overlap_threshold = .7
        match_threshold = .8

        buckets = []                

        b = 0

        DEBUG = False

        rects = set(rects)

        for rect in rects:
            A = []

            if DEBUG: print(F"[{b}]: {rect}")
            b+=1

            for i in range(len(buckets)):
                

                # count number of rectangles in bucket whose overlapping area with rect exceeds the threshold
                count = sum(((OverlappingArea(rect, other) / max(rect.Area(), other.Area())) >= overlap_threshold) for other in buckets[i])
                ratio = (count / len(buckets[i]))
                
                if DEBUG:
                    print(F"\t({i}): {' | '.join(str(r) for r in buckets[i])}")
                    for other in buckets[i]:
                        print(F"\t\t{rect.Area()} {other.Area()} {OverlappingArea(rect,other)} | {OverlappingArea(rect,other)/(max(rect.Area(),other.Area()))}")

                    print(F"\t\tMATCHED: {count} ({ratio})")
                
                # add the bucket to the list of options if at least over 80% of the rectangles in this bucket overlap 
                if ratio > match_threshold: A.append([ratio, i])                    
            
            # Add the rectangle to the bucket with the best match ratio. If none were valid, create a new bucket
            if A: buckets[ max(A)[1] ].append(rect)
            else: buckets.append([ rect ])

        if DEBUG:
            print('_'*20)        
            print("BUCKETS:")       

        # Low variance filter        
        var_threshold = 0.006

        normalized = [bucket for bucket in buckets]
        
        for i in range(len(buckets)):            

            if DEBUG:
                print(F"[{i}]: {' | '.join(str(r) for r in buckets[i])}")
                print(F"       {' | '.join(str(int(r)) for r in buckets[i])}")
            
            # Convert rects to bitmasks and normalize their values
            normalized[i] = [*map(int, normalized[i])]
            normalized[i] = [Normalize(val, min(normalized[i]), max(normalized[i])) for val in normalized[i]]            

            if DEBUG:
                for r in normalized[i]: print('\t' + str(r))        

                print(F"\t\tMEAN: {np.array(normalized[i]).mean()}")
                print(F"\t\tVAR:  {np.array(normalized[i]).var()}")

        #buckets = filter(lambda bucket: np.array(bucket).var() > var_threshold, buckets)
        #                 
        result = []
        max_var = var_threshold

        for i in range(len(buckets)):
            var = np.array(normalized[i]).var() 
            if var > max_var:
                max_var = var
                result = buckets[i]


        return result





"""==============================================================="""

class Rect(object):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0    

    display_color = None

    def __init__(self, rect, color = (0, 255, 0)):
        
        if type(rect) is int:
            self.x1 = rect & 0x1fff; rect >>= 13
            self.y1 = rect & 0x1fff; rect >>= 13
            self.x0 = rect & 0x1fff; rect >>= 13
            self.y0 = rect & 0x1fff
        else:
            (x, y, w, h) = rect
            self.x0 = int(x)
            self.y0 = int(y)
            self.x1 = int(x + w)
            self.y1 = int(y + h)

        self.display_color = color
        
    def Display(self, frame):
        cv2.rectangle(frame, (self.x0, self.y0), (self.x1, self.y1), self.display_color, 2)

    def Area(self):
        return (self.x1 - self.x0) * (self.y1 - self.y0);


    """ Comparisons """

    def __lt__(self, rect):
        return [self.y0, self.x0, self.y1, self.x1] \
             < [rect.y0, rect.x0, rect.y1, rect.x1]

    def __gt__(self, value):
        return [self.y0, self.x0, self.y1, self.x1] \
             < [rect.y0, rect.x0, rect.y1, rect.x1]

    def __eq__(self, rect):
        return [self.y0, self.x0, self.y1, self.x1] \
            == [rect.y0, rect.x0, rect.y1, rect.x1]

    def __ne__(self, rect):
        return (self == rect) == False

    """ Parsing """

    def __str__(self):
        return F"[({self.x0},{self.y0}) => ({self.x1},{self.y1})]"

    def __hash__(self):
        return int(self)

    # Converts rectangle coordinates to a bitmask representation    
    def __int__(self):
        """
        Notes:

        If we account for the highest possible monitor resolution currently in existence (8K), we can safely assume that the greatest possible value 
        for any dimension in (x0, y0, x1, y1) would require at most 13 bits (0b1111111111111 = 8191), meaning the highest value returned by this 
        function could have 13*4 = 52 bits (restricted to "real" data (i.e., 1 pixel in lower righthand corner of a 7680x4320 monitor), the maximum 
        value would be 0b1110111111111100001101111111101111111111000011011111, 4221864800940255 in base 10). 
        
        Because variance calculation requires squaring, these numbers could exceed 64 bits in the worst case. Thankfully, Python handles integers of arbitrary length,
        so this is no problem

        Values in mask correspond to (y0, x0, y1, x1), or more intuitively, (top row, left column, bottom row, right column)
        """
        mask = 0

        for val in [self.y0, self.x0, self.y1, self.x1]:
            mask <<= 13
            mask |= val

        return mask
