import time
import threading
import array
import logging

#import pymaging_bmp.bmp
import pymaging_png.png
import pymaging_jpg.jpg
import pymaging.formats
#pymaging.formats.register(pymaging_bmp.bmp.BMP)
pymaging.formats.register(pymaging_png.png.PNG)
pymaging.formats.register(pymaging_jpg.jpg.JPG)

import pymaging.image
from pymaging.pixelarray import get_pixel_array
from pymaging.colors import RGB

class Image(pymaging.image.LoadedImage):
    @classmethod
    def convertImage(cls, img):
        img = cls(img.mode, img.width, img.height, img.pixels, img.palette)
        img.size = (img.width, img.height)
        #pymaging.image.Image.save(img, open("%s.png"%time.time(), "wb"), "png")
        return img

    @classmethod
    def open(cls, file, *args):
        if len(args):
            mode = args[0]
            img = pymaging.image.LoadedImage.open(open(file, mode))
        else:
            img = pymaging.image.LoadedImage.open(open(file, "rb"))
        return cls.convertImage(img)

    def save(self, outfile):
        format = None
        if outfile.lower().endswith(".png"):
            format = "png"
        elif outfile.lower().endswith(".jpg") or outfile.lower().endswith(".jpeg"):
            format = "jpg"
        elif outfile.lower().endswith(".bmp"):
            format = "bmp"
        if not format:
          raise Error("Unknown image format was detected: %s"%outfile)
        return pymaging.image.Image.save(self, open(outfile, "wb"), format)

    @classmethod
    def fromstring(cls, mode, size, data, *args):
        decoder = args[0]
        decodemode = args[1]
        if decoder.lower()!="raw":
            raise Error("Only RAW source data is supported: decoder->%s"%decoder)
        if mode.lower()!="rgb":
            raise Error("Only RGB mode is supported: mode->%s"%mode)
        
        image_bytes = None
        if decodemode.lower()=="rgb":
            image_bytes = array.array("B", data)
        elif decodemode.lower()=="rgbx":
            original_bytes = array.array("B", data)
            image_bytes = array.array("B", [0,]*(len(data)*3/4))
            def func(org, dst, c):
                for i in xrange(len(org)/4):
                    dst[c+3*i] = org[c+4*i]
            threads = []
            for col in xrange(3):
                t = threading.Thread(target=func, args=(original_bytes, image_bytes, col))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            #image_bytes = array.array("B", "")
            #for i in xrange(len(original_bytes)):
            #    if i%4==3:
            #        continue
            #    else:
            #        image_bytes.append(original_bytes[i])
        else:
            raise Error("Unexpected decode mode: decodemode->%s"%decodemode)
          
        pixels = get_pixel_array(image_bytes, size[0], size[1], 3)
        img = cls(RGB, size[0], size[1], pixels)
        img.size = size
        return img
    
    def paste(self, *args):
        if not issubclass(args[0].__class__, pymaging.image.Image):
            logging.warn("Do nothing because only Image update is implemented in paste().")
        else:
            if len(args)==3:
                logging.warn("Mask will be ignored: %s"%args[2])
            img = args[0]
            box = args[1]
            if box is None:
                box = (0, 0)
            elif len(box)==4:
                img.resize(box[0]-box[2], box[1]-box[3])
                box = (box[0], box[1])
            if len(box)!=2:
                raise Error("Unexpected box was given: %s"%box)
            self.blit(box[0], box[1], img)
            #pixels = self.pixels
            #img_pixels = img.pixels
            #for x in xrange(img.width):
            #    for y in xrange(img.height):
            #        pixels.set(box[0]+x, box[1]+y, img_pixels.get(x, y))
            
    def histogram(self):
        pixelsize = self.pixelsize
        data = self.pixels.data
        histo = array.array("L", [0,]*256*pixelsize)

        #for d in data:
        #    histo[d] += 1
        #histo = [0,]*(256*pixelsize)
        #col_data = zip(*[data[x:x+pixelsize] for x in xrange(0, len(data)-1, pixelsize)])
        #for col in xrange(pixelsize):
        #    for i in xrange(256):
        #        histo[i+256*col] = col_data[col].count(i)
        def func(d, h, c, n):
            offset = 256*c
            for i in xrange(c, len(d), n):
                h[d[i]+offset] +=1
        threads = []
        for col in xrange(pixelsize):
            t = threading.Thread(target=func, args=(data, histo, col, pixelsize))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        #col=0
        #for d in data:
        #    histo[d+256*col] +=1
        #    col = (col+1)%pixelsize
        return histo

    def crop(self, box):
        img = pymaging.image.Image.crop(self, box[2]-box[0], box[3]-box[1], box[1], box[0])
        return Image.convertImage(img)


