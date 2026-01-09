'''
| 
| Authors:      Ahmad Khoureich Ka
| Date:         01/2026
|
'''
from charm.toolbox.pairinggroup import PairingGroup
from msel import MSEL

from PIL import Image, ImageDraw
import io

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

    # encryption
    # msg = ./images/test_img.jpg
    areas_coordinates = [(249, 77, 400, 96), (121, 177, 271, 195), (664, 201, 873, 225), (55, 227, 561, 253),
                (479, 304, 568, 326), (57, 328, 568, 351), (55, 456, 298, 526), (680, 251, 936, 428)]
    M = get_M(areas_coordinates) # M = (m_0, ... ,m_8), where m_0 is the redacted image (see get_M function for more details)

    '''
    Selection function pi: M = (m_0, ... ,m_8) -> B_4 = (e_0, ... ,e_3). 
    pi(M[0]) = e_0 of B_4, etc.
    pi(M[1]) = e_1 of B_4, etc.
    '''    
    pi = [0, 1, 1, 1, 1, 1, 1, 2, 2] 
    
    # encrypt M under the selection function pi
    C = msel.encrypt(mpk, pi, M)

    # generate a key for selection vector x
    '''
    By default, the first component of x is 1 to allow decryption of the redacted image m_0.
    The last component is not used, see comments on lines 16-17.
    '''
    x = [1, 0, 0, 0] 
    SKx = msel.keyder(msk, x)

    # decrypt the ciphertext C with SKx
    decrypted_M = msel.decrypt(SKx, C) 
    m_0 = io.BytesIO(decrypted_M[0])
    img_0 = Image.open(m_0)

    for m_i in decrypted_M[1:]:
        idx = m_i.find(b')')
        left_upper_point = m_i[:idx+1].decode(encoding='utf-8')
        img_i = io.BytesIO(m_i[idx+1:])
        img_i = Image.open(img_i)
        img_0.paste(img_i, eval(left_upper_point))

    img_0.show()
    
def get_M(areas):
    M = []
    image = Image.open('./images/test_img.jpg')
    draw = ImageDraw.Draw(image)

    for area in areas:
        img_i = image.crop(area)
        img_i_byte = io.BytesIO()
        img_i.save(img_i_byte, format='JPEG')
        left_upper_point = f"({area[0]},{area[1]})"
        m_i = left_upper_point.encode(encoding='utf-8') + img_i_byte.getvalue()
        M.append(m_i)
        area = (area[0], area[1], area[2]-1, area[3]-1)  # Adjust area to avoid boundary issues
        draw.rectangle(area, fill=(0, 0, 0))

    img_byte = io.BytesIO()
    image.save(img_byte, format='JPEG')
    M.insert(0, img_byte.getvalue())  # Add the redacted image as the first element of M
    # pi.insert(0, 0)  # Corresponding selection for redacted image

    return M

if __name__ == "__main__":
    main()