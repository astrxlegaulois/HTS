from Crypto.Cipher import Blowfish
from Crypto import Random
from struct import pack
import base64
import hashlib
bs = Blowfish.block_size
keystr = b'This is key'
keykey = hashlib.sha1()
keykey.update(keystr)
key=keykey.hexdigest()
iv = Random.new().read(bs)
cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
plaintext = b'This is plain text'
plen = bs - divmod(len(plaintext),bs)[1]
padding = [plen]*plen
padding = pack('b'*plen, *padding)
msg = iv + cipher.encrypt(plaintext + padding)
encoded = base64.b64encode(msg)
print encoded
