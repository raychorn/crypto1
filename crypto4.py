import os
import sys
import json
import uuid
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
        if (self.row == len(self.pages)) and (self.col == len(self.pages[-1])):
            raise IndexError('Slicer has completed.')
        the_slice = []
        for i in range(n):
            the_slice.append(self.pages[self.row][self.col])
            self.row += 1
            if (self.row == len(self.pages)):
                self.col += 1
                if (self.col == len(self.pages[-1])):
                    return the_slice
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
    
    uu = uuid.uuid4()
    print(uu)
    uu_hex = str(uu)
    print(uu_hex)

    hexlify = lambda x:hex(int('0xffff', 0) - x).split('0x')[-1]
    slicer = Slicer(pages=pages)
    count = 0
    byte_count = 0
    uuids = []
    while (1):
        __u__ = uu = str(uuid.uuid4())
        t = __u__.split('-')[0]
        try:
            aSlice = slicer.slice(len(t))
        except IndexError as ex:
            print(ex)
            break
        m = len(''.join(aSlice))
        print('*** t -> {}, t[0:{}] -> {}, ''.join(aSlice) -> {}, t[-{}:] -> {}'.format(t, m, t[0:m], ''.join(aSlice), m, t[-m:]))
        __u__ = __u__.replace(t, (''.join(aSlice)+t[-m:])[0:m])
        __u__ = __u__.replace(__u__[-4:], hexlify(count))
        assert len(uu) == len(__u__), 'Problem with the UUID. Expected {} bytes but got {} bytes.'.format(len(uu), len(__u__))
        print('{} -> {} -> {}'.format(uu, aSlice, __u__))
        uuids.append(__u__)
        count += 1
        byte_count += len(aSlice)
    print('Counted {} slices for {} bytes.'.format(count, byte_count))
    assert byte_count == len(encrypted), 'Problem with the slicer?  Expected {} bytes but counted {}.'.format(len(encrypted), byte_count)
    
    d = {}
    for i in range(0, len(uuids), 2):
        d[uuids[i]] = uuids[i+1]
    print(json.dumps(d, indent=3))