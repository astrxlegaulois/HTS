from crypt_1 import encryptString

def proba_somme(p1,p2):
	ans = {}
	for i, val1 in p1.items():
		for j, val2 in p2.items():
			if i+j not in ans.keys():
				ans[i+j] = 0
			ans[i+j] += val1*val2
	return ans

def md5tot_proba():
	p = {}
	for i in range(16):
		p[i] = 1./16
	for j in range(5):
		p = proba_somme(p,p)
	return p

def normalize(p):
	tot = 0
	for k in p.keys():
		tot += p[k]
	for k in p.keys():
		p[k] = p[k]/tot

def pass_proba(enc, char=None,char_ord=None, init=None):
	if (char is not None and char_ord is not None) or (char is None and char_ord is None):
		raise IOError
	elif char_ord is None:
		char_ord = ord(char)
	if init is None:
		init = {}
		for i in range(16):
			init[i] = 1./16
	tot_p = md5tot_proba()
	ans = {}
	for k in init.keys():
		ans[k] = init[k]*tot_p[-enc+char_ord+k]
	normalize(ans)
	return ans

print pass_proba(char='-',enc=-89)

#def get_pass_proba(enc,char):

#class proba
#+
#-
#* avec poids
#renorm
#
#class proba char
#
#class probachar fixed
#
#class proba_pass