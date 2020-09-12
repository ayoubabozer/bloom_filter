# Bloom Filter

A [Bloom Filter](https://en.wikipedia.org/wiki/Bloom_filter)  is a space-efficient probabilistic data structure. conceived by Burton Howard Bloom in 1970, that is used to test whether an element is a member of a set. False positive matches are possible, but false negatives are not – in other words, a query returns either "possibly in set" or "definitely not in set". Elements can be added to the set, but not removed (though this can be addressed with the counting Bloom filter variant); the more items added, the larger the probability of false positives.


## Usage

```python
from bloom.bloom_filter import BloomFilter

bloom = BloomFilter(1000, 0.001)

bloom.add('Ayoub') #adds 'Ayoub' to the BloomFilter

bloom.add('Edleen') #adds 'Edleen' to the BloomFilter

len(bloom) #returns 2

#adds a vector of items to the BloomFilter
bloom.add_vector(['Hani', 'Naya', 'Alma'])

len(bloom) #returns 5

'Ayoub' in bloom #returns True

```

### Thanks

