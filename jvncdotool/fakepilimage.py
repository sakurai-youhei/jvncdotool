import time

#import pymaging_bmp.bmp
import pymaging_png.png
import pymaging_jpg.jpg
import pymaging.formats
#pymaging.formats.register(pymaging_bmp.bmp.BMP)
pymaging.formats.register(pymaging_png.png.PNG)
pymaging.formats.register(pymaging_jpg.jpg.JPG)

import pymaging.image

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
        import array
        from pymaging.pixelarray import get_pixel_array
        from pymaging.colors import RGB
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
            image_bytes = array.array("B", "")
            for i in xrange(len(original_bytes)):
                if i%4==3:
                    continue
                else:
                    image_bytes.append(original_bytes[i])
        else:
            raise Error("Unexpected decode mode: decodemode->%s"%decodemode)
          
        pixels = get_pixel_array(image_bytes, size[0], size[1], 3)
        img = cls(RGB, size[0], size[1], pixels)
        img.size = size
        return img
    
    def paste(self, *args):
        import logging
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
            for x in xrange(img.width):
                for y in xrange(img.height):
                    self.set_color(box[0]+x, box[1]+y, img.get_color(x, y))
            
    def histogram(self):
        histo = [0,]*(255*self.pixelsize)
        for x in xrange(self.width):
            for y in xrange(self.height):
                col = self.get_color(x, y)
                histo[col.red] +=1
                histo[256+col.green] +=1
                histo[256+256+col.blue] +=1
                if self.pixelsize==4:
                    histo[256+256+256+col.alpha] +=1
        return histo

    def crop(self, box):
        img = pymaging.image.Image.crop(self, box[2]-box[0], box[3]-box[1], box[1], box[0])
        return Image.convertImage(img)


