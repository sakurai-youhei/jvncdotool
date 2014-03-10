
#import pymaging_bmp.bmp
import pymaging_png.png
import pymaging_jpg.jpg
import pymaging.formats
#pymaging.formats.register(pymaging_bmp.bmp.BMP)
pymaging.formats.register(pymaging_png.png.PNG)
pymaging.formats.register(pymaging_jpg.jpg.JPG)

import pymaging.image

class Image(pymaging.image.Image):
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
        return pymaging.image.Image.save(open(outfile, "wb"), format)

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
        img = Image.LoadedImage(RGB, size[0], size[1], pixels)
        img.size = size
        return img
    
    def paste(self, *args):
        import logging
        logging.warn("Do nothing because paste() is not implementated, yet: %s"%args)
