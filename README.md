# M-Sel
Message Selection functional encryption (M-Sel)[1] is a practical application of Inner-Product Functional Encryption (IPFE)[2] which allows users to decrypt selected portions of a ciphertext. The plaintext is partitioned into a set of messages M = {m1, . . . , mt}. The encryption of M consists in encrypting each of its elements using distinct encryption keys. A user with a functional decryption key skx derived from a selection vector x can access a subset of M from the encryption thereof and nothing more.

## Prerequisites
The scheme is implemented in Python 3.7.17 using the Charm framework [3] version 0.50. The Python Pillow Library is also used.

## References
[1] Ahmad K. Ka. M-Sel: A message selection functional encryption from simple tools. In Mark Manulis, Diana MaimuŢ, and George Teşeleanu, editors, Innovative Security Solutions for Information Technology and Communications, pages 79–96, 2024. An updated version available on ePrint Archive, Report [2024/1958](https://eprint.iacr.org/2024/1958)<br/>
[2] Abdalla, M., Bourse, F., De Caro, A., Pointcheval, D.: Simple functional encryption schemes for inner products. In: Katz, J. (ed.) Public-Key Cryptography – PKC 2015. pp. 733–751. Springer Berlin Heidelberg (2015)<br/>
[3] J. A. Akinyele, C. Garman, I. Miers, M. W. Pagano, M. Rushanan, M. Green, and A. D. Rubin. Charm: a framework for rapidly prototyping cryptosystems. Journal of Cryptographic Engineering, pages 111–128, 2013<br/>

