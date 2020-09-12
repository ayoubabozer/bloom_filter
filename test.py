from unittest import TestCase, main
from bloom.bloom_filter import BloomFilter

class TestBloomFilter(TestCase):
    
    """
    Testing BloomFilter membership
    """
    def test_membership(self):
        
        bloom = BloomFilter(1000, 0.001)
        anaplan = 'Anaplan'
        bloom.add(anaplan)
        self.assertTrue(anaplan in bloom)
        self.assertFalse('new' in bloom)
        
    """
    Testing BloomFilter vector membership
    """
    def test_vector_membership(self):
        
        bloom = BloomFilter(1000, 0.001)
        v = ['Anaplan', 1, 2, 3]
        bloom.add_vector(v)
        self.assertTrue(bloom.contains_vector(v))
        self.assertFalse(bloom.contains_vector([1, 2, 3, 4]))

if __name__ == '__main__':
    main()