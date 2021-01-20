import os
import sys

import random

lib3 = '/workspaces/private_vyperlogix_lib3'
if (not any([f.find(lib3) > -1 for f in sys.path])):
    sys.path.insert(0, lib3)
    
from vyperlogix.crypto import utils as crypto_utils

for f in sys.path:
    print(f)
    

class Pager():
    def __init__(self, items, siz):
        self.siz = siz
        self.items = items
        self.num = len(items)
        self.pg = 0
        self.num_per_page = int(self.num / self.siz)

    @property
    def page(self):
        j = int(self.num_per_page*self.pg)
        items = self.items[j:j+self.num_per_page]
        self.pg += 1
        return items

    def pageNum(self, n):
        j = int(self.num_per_page*n)
        items = self.items[j:j+self.num_per_page]
        return items

    @property
    def pages(self):
        return int(self.num / self.num_per_page)


if (__name__ == '__main__'):
    def func(plaintext=None, decrypted_decoded_text=None):
        print('(f) plaintext={}, decrypted_decoded_text={}'.format(plaintext, decrypted_decoded_text))
        assert plaintext == decrypted_decoded_text, 'Problem with the crypto?  Expected "{}" got "{}".'.format(plaintext, decrypted_decoded_text)
    
    plaintext = 'this is supposed to be a secret.'
    encrypted = crypto_utils.encrypt(plaintext, callback=func)
    print('(1) plaintext: {}, encrypted: {}'.format(plaintext, encrypted))

    p = Pager(encrypted, len(encrypted)/4)

    p = Pager([i for i in range(100)], 10)
    for i in range(p.pages):
        print(p.page)
        
    j = 0
    k = 5
    while (j < k):
        n = random.randint(0, p.pages)
        print(p.pageNum(n))
        j += 1
