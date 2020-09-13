
####################### Import Libraries #################################

import numpy as np
from math import log, ceil, floor
import sklearn.utils.murmurhash as mu
##########################################################################


####################### Hash Generator ###################################

def get_hash_generator(repeat: int=1):
    """
    A closure providing python function which generates
    repeated hash function with different
    seeds to give different hash codes.

    Parameters:

        :param repeat: num repreated hash functions.
        :type repeat: int.

    Returns:

        :returns: python function which generates
                repeated hash function.
        :rtype: function
    """
    def hash_generator(item: object):

        # encdoe items for data type generalization.
        item = str(item).encode('utf-8')

        for index in range(repeat):
            yield mu.murmurhash3_32(item, seed=index)

    return hash_generator
##########################################################################


####################### BitArray Class ###################################

class BitArray():

    """
    A compact data structure represents an array of zeros and ones.
    Instance is initialized by the size of the array - num of
    elements in the array defined as zeros.

    Parameters:

        :param size: num of intialized zeros of the array.
        :type size: int.

    Attributes:

        :capacity : num of items to store.
        :arr : numpy array represents BitArray data structure.
    """

    def __init__(self, size:int):

        if not (size > 0):
            raise ValueError("size of BitArray must be greater than 0.")

        self.size = size
        self.arr = np.zeros(self.size, dtype=np.bool)


    def fill(self, index:int):

        """
        fill one in the given index.

        Parameters:

            :param index: the specified index to fill.
            :type index: int.
        """
        self.arr[index] = 1

    def __len__(self) -> int:

        """
        implementation of the magic length method - which returns num of 
        ones stored in the array.

        Parameters:

            :returns: num of ones in the array.
            :rtype: int.
        """
        return self.arr.sum()

    def __getitem__(self, index:int) -> int:

        """
        implementation of the getitem magic method - which returns the 
        value stored in a particular index.

        Parameters:
            :param index: the specified index to get.
            :type index: int. 

        Returns:

            :returns: num of ones in the array.
            :rtype: int
        """
        return self.arr[index]

    def __iter__(self):

        """
        implementation of the magic iter method - which returns an iterator
        over the array.

        Returns:
            :returns: BitArray iterator.
            :rtype: iterator.
        """
        return iter(self.arr)

    def __str__(self) -> str:

        """
        implementation of the magic str method - which returns a
        string representation for the BitArray.

        Returns:

            :returns: BitArray representation.
            :rtype: str.
        """
        return self.arr.__str__()
##########################################################################


####################### BloomFilter Class ################################
class BloomFilter():

    """
    A space-efficient probabilistic data structure.
    which designed to answer rapidly and memory-efficiently, whether an element
    is present in the BloomFilter.
    The price paid for this efficiency is that a BloomFilter is a probabilistic data structure:
    it tells us that the element either definitely is not present or may be present - flase
    positive probability.

    Instance is initialized by the capacity and false positive probability.

    Parameters:

        :param capacity: the desired error rate of the filter false positives.
        :type capacity: int.

        :param false_positive_prob: the desired num of elements to store in the BloomFilter.
        :type false_positive_prob: float.
        :default false_positive_prob : 0.05

    Attributes:

        :capacity : num of desired items to store.
        :false_positive_prob : desired false positive probability
        :bits : optimal num of bits in the BloomFilter.
        :bit_arr : BitArray represents the BloomFilter data structure,
        :k_hash_functions : optimal number of hash functions to use.
        :hash_generator: python generator yeilding k hashed code for an item.
    """

    def __init__(self, capacity, false_positive_prob=0.05):

        if not (0 < false_positive_prob < 1):
            raise ValueError("false_positive_prob must be between 0 and 1.")

        if not capacity > 0:
            raise ValueError("BloomFilter capacity must be greater than zero. ")

        self.capacity = capacity
        self.false_positive_prob = false_positive_prob
        self.bits = self.get_optimal_bits()
        self.bit_arr = BitArray(self.bits)
        self.k_hash_functions = self.get_optimal_hash_functions()
        self.hash_generator = get_hash_generator(self.k_hash_functions)

    def get_optimal_hash_functions(self) -> int:

        """
        calculates the optimal number of hash functions to use,
        based on desired false positive probabilty.

        # math #
        k = -log(p)

        Returns:

            :returns: num of optimal hash functions.
            :rtype: int
        """

        return ceil(
            -1 * log(self.false_positive_prob,2)
        )

    def get_optimal_bits(self) -> int:

        """
        calculates the optimal number of bits to use,
        based on capacity and desired false positive probabilty.

        # math #
        m = -n*ln(p)/ln(2)^2

        Returns:

            :returns: num of optimal bits.
            :rtype: int
        """


        return  ceil(
            -1 * self.capacity * log(self.false_positive_prob)
            / (log(2)**2)
        )

    def get_estimated_items(self) -> int :

        """
        calculates estimated number of elements stored in BloomFilter.

        # math #
        let X : num of ones in BloomFilter.
        n* = -m/k*ln(1-X/m)

        Returns:

            :returns: estimated num of stored items.
            :rtype: int
        """

        num_ones = len(self.bit_arr)

        return  abs(floor(
                -1 *  (self.bits / self.k_hash_functions)
                * log(1 - (num_ones / self.bits))
                ))


    def validate_item(self, item:object):

        """
        validates that item must be str, int or float.

        Parameters:

            :item : item to validate.
            :type item : object
        """

        if(not isinstance(item, (str, int, float))):
             raise TypeError("Item must be str, int or float.")


    def validate_vector(self, vector:object):

        """
        validates that vector must be list.

        Parameters:

            :vector : vector to validate.
            :type item : object
        """

        if(not isinstance(vector, list)):
             raise TypeError("Vector must be of type list.")

    def add(self, item:object):

        """
        adds item to BloomFilter.

        Parameters:

            :item : item to add.
            :type item : object (str | int | float)
        """


        self.validate_item(item)

        for hash_code in self.hash_generator(item):
            self.bit_arr.fill(hash_code % self.bits)

    def search(self, item:object) -> bool:

        """
        searchs item in BloomFilter.

        Parameters:

            :item : item to search.
            :type item : object (str | int | float)

        Returns:

            :returns: False if the item definitely is not in BloomFilter
                        otherwise, return True.
            :rtype: bool
        """

        self.validate_item(item)

        return all(
            self.bit_arr[hash_code%self.bits]
            for hash_code in self.hash_generator(item)
        )

    def contains(self, item:object) -> bool:

        """
        check if BloomFilter contains an item.

        Parameters:

            :item : item to check.
            :type item : object (str | int | float)

        Returns:

            :returns: False if the item is definitely not in BloomFilter
                        otherwise, return True.
            :rtype: bool
        """

        return self.search(item)

    def len(self) -> int:

        """
        Returns an estimation of stored items in BloomFilter.

        Returns:

            :returns: estimation of stored items in BloomFilter.
            :rtype: int.
        """

        return self.get_estimated_items()

    def add_vector(self, vector:list):

        """
        adds all items in the vector to BloomFilter.

        Parameters:

            :item : vector to add.
            :type vector : list

        """

        self.validate_vector(vector)

        for item in vector:
            self.add(item)


    def contains_vector(self, vector:list) -> bool:

        """
        Checks if BloomFilter contains all items in a  vector.

        Parameters:

            :vector : vector to check.
            :type vector : list.

        Returns:

            :returns: False if at least one item in the vector is definitely not in BloomFilter
                        otherwise, return True.
            :rtype: bool
        """

        self.validate_vector(vector)

        return all(self.contains(item) for item in vector)

    def __iter__(self):

        """
        implementation of the magic iter method - which returns an
        iterator over the BloomFilter.

        Returns:

            :returns: BloomFilter iterator.
            :rtype: iterator.
        """
        return iter(self.bit_arr)

    def __len__(self) ->int :

        """
        implementation of the magic len method - which returns an
        estimation of stored items in BloomFilter.

        Returns:

            :returns: estimation of stored items in BloomFilter.
            :rtype: int.
        """
        return self.len()

    def __contains__(self, item:object) -> bool:

        """
        implementation of the magic contains method - which returns a
        False if the item is definitely not in BloomFilter
        otherwise, return True.

        Returns:

            :returns: False if the item is definitely not in BloomFilter
                        otherwise, return True.
            :rtype: bool.
        """

        return self.contains(item)

    def __str__(self):

        """
        implementation of the magic str method - which returns a
        string representation for the BloomFilter.

        Returns:

            :returns: BloomFilter representation.
            :rtype: str.
        """
        return self.bit_arr.__str__()        
##########################################################################
