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
    
    def __repr__(self):
        return 'siz={}, num={}, pg={}, num_per_page={}, items={} {}'.format(self.siz, self.num, self.pg, self.num_per_page, len(self.items), self.items)


class Slicer():
    def __init__(self, pages=[]):
        self.pages = pages
        self.row = 0
        self.col = 0
        
    def this(self):
        return self
        
    def slice(self, n):
        the_slice = []
        for i in range(n):
            the_slice.append(self.pages[self.row][self.col])
            self.row += 1
            if (self.row == len(self.pages)):
                self.col += 1
                self.row = 0
        return the_slice
    
    def reset(self, num_per_page, num_pages):
        self.row = 0
        self.col = 0
        self.num_pages = num_pages
        self.num_per_page = num_per_page
        self.pages = []
        for i in range(self.num_pages):
            self.pages.append([])
        return self
    
    def unslice(self, item):
        self.pages[self.row].append(item)
        self.row += 1
        if (self.row == len(self.pages)):
            self.col += 1
            self.row = 0

    def __repr__(self):
        return 'row={}, col={}, num_pages={}, num_per_page={}, pages={}'.format(self.row, self.col, self.num_pages, self.num_per_page, self.pages)


if (__name__ == '__main__'):
    def func(plaintext=None, decrypted_decoded_text=None):
        print('(f) plaintext={}, decrypted_decoded_text={}'.format(plaintext, decrypted_decoded_text))
        assert plaintext == decrypted_decoded_text, 'Problem with the crypto?  Expected "{}" got "{}".'.format(plaintext, decrypted_decoded_text)
    
    plaintext = 'this is supposed to be a secret.'
    encrypted = crypto_utils.encrypt(plaintext, callback=func)
    print('(1) plaintext: {}, encrypted: {}'.format(plaintext, encrypted))
    print('-'*30)
    print()

    pager = Pager(encrypted, 12)
    print(pager)

    j = 0
    k = pager.pages
    pages = []
    while (j < k):
        pages.append(pager.pageNum(j))
        j += 1
    j = 1
    for aPage in pages:
        print('{} -> {} {}'.format(j-1, len(aPage), aPage))
        j += 1
        
    slicer = Slicer(pages=pages)
    aSlice = slicer.slice(10)
    print(aSlice)
    
    new_slicer = Slicer().this().reset(16, 12)
    for item in aSlice:
        new_slicer.unslice(item)
    print(new_slicer)
