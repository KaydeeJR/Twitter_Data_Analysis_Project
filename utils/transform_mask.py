import numpy as np

class MaskTransformation:
    """
    A class which transforms a given image mask.
    
    The mask is then transformed into an appropriate mask.
    
    The way the masking functions works is that it requires all white part of the mask should be 255 not 0 (integer type). This value represents the "intensity" of the pixel. Values of 255 are pure white, whereas values of 1 are black. Here, you can use the provided function below to transform your mask if your mask has the same format as above. Notice if you have a mask that the background is not 0, but 1 or 2, adjust the function to match your mask.
    """
    def __init__(self):
        pass

    def transform_values(self, val):
        """
        This function swaps number 0 to 255.
        
        :param val: list
        
        :return: list of modified values
        """
        for v in range(len(val)):
            if val[v] == 0:
                val[v]= 255
        
        return val

    def transform_mask(self, mask):
        """
        Transform the mask into a new one that will work with the function.

        :param mask: a matrix containing values of the image mask
        
        :return: transformed matrix of values
        """
        transformed_mask = np.ndarray((mask.shape[0], mask.shape[1]), object)

        for i in range(len(mask)):
            transformed_mask[i] = list(map(self.transform_values, mask[i]))
    
        return transformed_mask