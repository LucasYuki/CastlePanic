from PIL import ImageTk, Image

class ImageHelper():
    @staticmethod
    def get_tk_image(image, width=None, height=None, 
                     max_width=None, max_height=None):
        if (width is None) and (height is None):
            width, height = image.size
        elif height is None:
            height = width//ImageHelper.get_proportion(image)
        elif width is None:
            width = int(height*ImageHelper.get_proportion(image))

        if (max_width is not None) and (max_width < width):
            height = int(height * max_width / width)
            width = max_width
        if (max_height is not None) and (max_height < height):
            width = int(width * max_height / height)
            height = max_height
        
        return ImageTk.PhotoImage(image.resize((width, height)))

    @staticmethod
    def get_proportion(image):
        width, height = image.size
        return width/height
