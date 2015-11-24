from crypt_1 import encryptString, CodeToDecrypt

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

def init_pass_p():
	init = {}
	for i in range(16):
		init[i] = 1./16
	return init

def init_clearchars_p(position):
	init = {}
	if position%32 in [3,7,11,15]:
		return {'-':1.}
	elif position%32 in [8]:
		return {'O':1.}
	elif position%32 in [9]:
		return {'E':1.}
	elif position%32 in [10]:
		return {'M':1.}
	elif position%32 in [16,18]:
		return {'1':1.}
	elif position%32 in [17]:
		return {'.':1.}
	elif position%32 in [19]:
		return {'\n':1.}
	else:
		for i in range(10):
			init[str(i)] = 1./36
		for i in range(ord('A'), ord('Z')+1):
			init[chr(i)] = 1./36
	return init

def update_pass_proba(enc, char=None,char_ord=None, init=None):
	if (char is not None and char_ord is not None) or (char is None and char_ord is None):
		raise IOError
	elif char_ord is None:
		char_ord = ord(char)
	if init is None:
		init = init_pass_p()
	tot_p = md5tot_proba()
	ans = {}
	for k in init.keys():
		ans[k] = init[k]*tot_p[-enc+char_ord+k]
	normalize(ans)
	return ans

#print update_pass_proba(char='-',enc=-89)

class ProbabilisticCode(CodeToDecrypt):
	def __init__(self, *args, **kwargs):
		CodeToDecrypt.__init__(self, *args, **kwargs)
		self.pass_p = []
		for i in range(32):
			self.pass_p.append(init_pass_p()) 
		self.md5tot_p = []
		self.clearchars_p = []
		for i in range(len(self.code)):
			self.md5tot_p.append(md5tot_proba())
			self.clearchars_p.append(init_clearchars_p(i))

	def compute_probas(self):
		for i in [j for j in range(len(self.code)) if j%20 in [4,7,8,9,10,11,15,16,17,18,19]]:
			self.pass_p[i%32] = update_pass_proba(enc=self.code[i], char=self.clearchars_p[i].keys()[0], init=self.pass_p[i%32])


md5_p = 'aef556ea6cba13581556ea6cba135815'
clearchars = '0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'
enc = encryptString(clearchars,md5_p=md5_p)

code = ProbabilisticCode(code=enc)

code.compute_probas()
print code.pass_p
#def get_pass_proba(enc,char):

#class proba
#+
#-
#* avec poids?
#renorm
#
#class proba char
#
#class probachar fixed
#
#class proba_pass