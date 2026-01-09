'''
| 
| Authors:      Ahmad Khoureich Ka
| Date:         01/2026
|
'''
from charm.toolbox.pairinggroup import PairingGroup
from msel import MSEL

def main():
    pairing_group = PairingGroup('MNT224')
    '''
    We actually use 3 vectors, but we define l=4. Therefore, we are safe as long as we distribute fewer than 4 vectors,
    whether they are linearly independent or not.
    '''
    l = 4

    # create an instance of MSEL
    msel = MSEL(pairing_group, l)

    # setup
    (msk, mpk) = msel.setup()

    '''
    encrypt a message M with selection function pi
    msg = 'This year, 650 pupils from schools X, Y, and Z each received two drops of polio vaccine.'
    '''    
    M = [b'This year,', b'650', b'pupils', b'from schools X, Y, and Z', b'each received', b'two drops of polio', b'vaccine.']
    # selection function pi: [0..t-1] -> [0..l-1], where t = |M|
    pi = [0, 2, 0, 1, 0, 2, 0]
    # pi(M[0]) = e_0 of B_4, pi(M[1]) = e_2 of B_4, etc.

    # encrypt M under the selection function pi
    C = msel.encrypt(mpk, pi, M)

    # generate a key for selection vector [1, 0, 0, 0]
    x = [1, 0, 0, 0]  # the last component is not used, see comments on lines 13-14.
    print("Selection Vector x:", x)
    SKx = msel.keyder(msk, x)
    # decrypt the ciphertext
    decrypted_M = msel.decrypt(SKx, C)
    decrypted_M = b' '.join(decrypted_M)
    print("Decrypted Message:", decrypted_M.decode('utf-8'))  

    # generate a key for selection vector [1, 1, 0, 0]
    x = [1, 1, 0, 0] 
    print("Selection Vector x:", x)
    SKx = msel.keyder(msk, x)
    # decrypt the ciphertext
    decrypted_M = msel.decrypt(SKx, C)
    decrypted_M = b' '.join(decrypted_M)
    print("Decrypted Message:", decrypted_M.decode('utf-8'))  

    # generate a key for selection vector [1, 1, 1, 0]
    x = [1, 1, 1, 0] 
    print("Selection Vector x:", x)
    SKx = msel.keyder(msk, x)
    # decrypt the ciphertext
    decrypted_M = msel.decrypt(SKx, C)
    decrypted_M = b' '.join(decrypted_M)
    print("Decrypted Message:", decrypted_M.decode('utf-8'))  

if __name__ == "__main__":
    main()



