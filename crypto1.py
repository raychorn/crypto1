import os
import sys

lib3 = '/workspaces/private_vyperlogix_lib3'
if (not any([f.find(lib3) > -1 for f in sys.path])):
    sys.path.insert(0, lib3)
    
from vyperlogix.crypto import utils as crypto_utils

for f in sys.path:
    print(f)


if (__name__ == '__main__'):
    def func(plaintext=None, decrypted_decoded_text=None):
        print('(f) plaintext={}, decrypted_decoded_text={}'.format(plaintext, decrypted_decoded_text))
        assert plaintext == decrypted_decoded_text, 'Problem with the crypto?  Expected "{}" got "{}".'.format(plaintext, decrypted_decoded_text)
    
    plaintext = 'this is supposed to be a secret.'
    encrypted = crypto_utils.encrypt(plaintext, callback=func)
    print('(1) plaintext: {}, encrypted: {}'.format(plaintext, encrypted))
    
    print('Single fold: folding {} bytes'.format(len(encrypted)))
    the_stuff = []
    i = 0
    for j in range(0, len(encrypted)+1, int(len(encrypted)/2)):
        stuff = encrypted[i:j]
        if (len(stuff)):
            print(stuff)
            the_stuff.append(stuff)
        i = j
    the_sum = sum([len(s) for s in the_stuff])
    assert the_sum  == len(encrypted), 'Problem with the fold (1). Expected {} but got {}.'.format(len(encrypted), the_sum)
    e =''.join([ch for ch in encrypted])
    for s in the_stuff:
        e = e.replace(s, '')
    assert len(e) == 0, 'Problem with the fold (2). Please check your logic.'
    print()
    print('Perform the fold.')
    print('Folding {} pages.'.format(len(the_stuff)))
    print(the_stuff[-1])
    print(the_stuff[0])
    folded_stuff = the_stuff[-1]+the_stuff[0]
    print(folded_stuff)
    assert len(folded_stuff) == len(encrypted), 'Problem with the fold (3). Please check your logic.'
    print()
    print('Try to decrypt:')
    p1 = crypto_utils.decrypt(encrypted)
    print('The original was decrupted -> "{}".'.format(p1))
    p2 = None
    try:
        p2 = crypto_utils.decrypt(folded_stuff)
        print('The original was decrupted -> "{}".'.format(p2))
    except:
        print('Failed due to an error.')
    assert p1 == p2, 'The fold worked and the decryption failed.'
