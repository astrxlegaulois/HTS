from crypt_1 import encryptString, generateClearCharsList, generatePasswordMD5
import random
import uuid

def gen_corpus(pot_char=generateClearCharsList(), pot_pass=generatePasswordMD5(), size=10**5):
	text = ''
	sep = '\nSEPARATOR\n'
	sep1 = '\nINNER_SEPARATOR\n'
	for step in range(size):
		clear = ''
		passw = ''
		for i in range(len(pot_char)):
			clear += random.choice(pot_char[i])
		for i in range(len(pot_pass)):
			passw += random.choice(pot_pass[i])
		enc = encryptString(clear,md5_p=passw)
		text += clear
		text += sep1
		text += passw
		text += sep1
		text +=	' '.join([str(el) for el in enc])
		text += sep
	with open('corpus'+str(uuid.uuid1())+'.txt','w') as f:
		f.write(text)

if __name__ == '__main__':
	gen_corpus()
