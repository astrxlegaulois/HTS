from crypt_1 import encryptString, decryptString, CodeToDecrypt, evalCrossTotal
import numpy as np
import md5

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

md5tot_p_init = md5tot_proba()

def normalize(p):
	tot = 0
	for k in p.keys():
		tot += p[k]
	for k in p.keys():
		p[k] = p[k]/tot

def init_pass_p():
	init = {}
	for i in range(16):
		init[hex(i)[2:]] = 1./16
	return init

def init_clearchars_p(position, chars):
	init = {}
	if position%20 in [3,7,11,15]:
		return {'-':1.}
	elif position%20 in [8]:
		return {'O':1.}
	elif position%20 in [9]:
		return {'E':1.}
	elif position%20 in [10]:
		return {'M':1.}
	elif position%20 in [16,18]:
		return {'1':1.}
	elif position%20 in [17]:
		return {'.':1.}
	elif position%20 in [19]:
		return {'\n':1.}
	else:
		for c in chars:
			init[c] = 1./len(chars)
	return init

def update_md5tot_proba(enc, chars_p, pass_p, init=None, weight=0):
	if init is None:
		init = md5tot_p_init
	ans = {}
	for p in pass_p.keys():
		for char in chars_p.keys():
			k = ord(char) + int(p,16) - enc
			if k not in ans.keys() and k in init.keys():
				ans[k] = 0.
				try:
					ans[k] += chars_p[char]*pass_p[p]
				except KeyError:
					if ans[k] == 0.:
						del ans[k]
				except ValueError:
					if ans[k] == 0.:
						del ans[k]
	normalize(ans)
	if weight != 0:
		for k in ans.keys():
			ans[k] = (init[k]**(weight/(1.+weight))) * (ans[k]**(1./(1+weight)))
	return ans

def update_md5tot_proba_forward(enc, init, passw, strng, weight=0, previous=None):
	if previous is None:
		return {evalCrossTotal(passw):1.}
	ans = {}
	for prev_k in previous.keys():

			k = evalCrossTotal(md5.new(strng).hexdigest()[0:16] + md5.new(str(prev_k)).hexdigest()[0:16])
			if k not in ans.keys() and k in init.keys():
				ans[k] = 0.
				try:
					ans[k] += previous[prev_k]
				except KeyError:
					if ans[k] == 0.:
						del ans[k]
	normalize(ans)
	if weight != 0:
		for k in ans.keys():
			ans[k] = (init[k]**(weight/(1.+weight))) * (ans[k]**(1./(1+weight)))
	return ans

def update_md5tot_proba_backward(enc, next, passw, strng):
	pass

def update_pass_proba(enc, chars_p, md5tot_p, init=None, weight=0):
	if init is None:
		init = init_pass_p()
	ans = {}
	for char in chars_p.keys():
		for md5_k in md5tot_p.keys():
			k = hex(md5_k + enc - ord(char))[2:]
			if k not in ans.keys() and k in init.keys():
				ans[k] = 0.
				try:
					ans[k] += chars_p[char]*md5tot_p[md5_k]
				except KeyError:
					if ans[k] == 0.:
						del ans[k]
	normalize(ans)
	if weight != 0:
		for k in ans.keys():
			ans[k] = (init[k]**(weight/(1.+weight))) * (ans[k]**(1./(1+weight)))
	return ans

def update_chars_proba(enc, pass_p, md5tot_p, init, weight=0):
	if len(init.keys()) == 1:
		return init
	ans = {}
	for k in pass_p.keys():
		for md5_k in md5tot_p.keys():
			try:
				char = chr(md5_k + enc - int(k,16))
				if char not in ans.keys() and char in init.keys():
					ans[char] = 0.
					try:
						ans[char] += pass_p[k]*md5tot_p[md5_k]
					except KeyError:
						if ans[char] == 0.:
							del ans[char]
			except ValueError:
				pass
	normalize(ans)
	if weight != 0:
		for k in ans.keys():
			ans[k] = (init[k]**(weight/(1.+weight))) * (ans[k]**(1./(1+weight)))
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
			self.md5tot_p.append(md5tot_p_init)
			self.clearchars_p.append(init_clearchars_p(i,chars=self.chars))

	def compute_pass_probas(self,weight=0,only_known=False):
		if only_known:
			seq = [i for i in range(len(self.code)) if i%20 in [3,7,8,9,10,11,15,16,17,18,19]]
		else:
			seq = range(len(self.code))
		for i in seq:
			self.pass_p[i%32] = update_pass_proba(enc=self.code[i], chars_p=self.clearchars_p[i], md5tot_p=self.md5tot_p[i], init=self.pass_p[i%32], weight=weight)

	def compute_chars_probas(self,weight=0):
		for i in range(len(self.code)):
			self.clearchars_p[i] = update_chars_proba(enc=self.code[i], init=self.clearchars_p[i], md5tot_p=self.md5tot_p[i], pass_p=self.pass_p[i%32], weight=weight)

	def compute_md5tot_probas(self,weight=0):
		for i in range(len(self.code)):
			self.md5tot_p[i] = update_md5tot_proba(enc=self.code[i], init=self.md5tot_p[i], pass_p=self.pass_p[i%32], chars_p=self.clearchars_p[i], weight=weight)

	def compute_md5tot_probas_forward(self, weight=0):
		self.md5tot_p[0] = update_md5tot_proba_forward(enc=self.code[i], init=self.md5tot_p[i+1], previous=None, passw=self.guess_pass(), strng=self.guess_string()[:i+1], weight=weight)
		for i in range(len(self.code)-1):
			self.md5tot_p[i+1] = update_md5tot_proba_forward(enc=self.code[i], init=self.md5tot_p[i+1], previous=self.md5tot_p[i], passw=self.guess_pass(), strng=self.guess_string()[:i+1], weight=weight)

	def compute_md5tot_probas_backward(self, weight=0):
		for i in [len(self.code)-j for j in range(len(self.code)-1)]:
			self.md5tot_p[i] = update_md5tot_proba_backward(enc=self.code[i], init=self.md5tot_p[i], next=self.md5tot_p[i+1], passw=self.guess_pass(), strng=self.guess_string()[:i+1], weight=weight)

	def guess_pass(self, maximum=True):
		try:
			pass_md5 = ''
			for i in range(32):
				items = self.pass_p[i].items()
				if not maximum:
					pass_md5 += np.random.choice([i for i,j in items], p=[j for i,j in items])
				else:
					p_max = max([j for i,j in items])
					pass_md5 += np.random.choice([i for i,j in items if j == p_max])
			return pass_md5
		except ValueError:
			return pass_md5

	def guess_string(self, maximum=True):
		try:
			ans = ''
			for i in range(len(self.code)):
				items = self.clearchars_p[i].items()
				if not maximum:
					ans += np.random.choice([i for i,j in items], p=[j for i,j in items])
				else:
					p_max = max([j for i,j in items])
					ans += np.random.choice([i for i,j in items if j == p_max])
			return ans
		except ValueError:
			return ans

	def decrypt(self, pass_md5):
		if len(pass_md5)<32:
			return ''
		return decryptString(self.code, md5_p=pass_md5)






md5_p = 'aef556ea6cba13581556ea6cba135815'
clearchars = '0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'
enc = encryptString(clearchars,md5_p=md5_p)

code = ProbabilisticCode(code=enc,chars=['0','D','Z'])
print 'guessed:    '+ code.guess_string()
#code.compute_md5tot_probas()#weight=1)
code.compute_pass_probas(only_known=True)#weight=1)
print 'original:'+md5_p
print 'guessed :'+code.guess_pass()
for i in range(100):
	code.compute_chars_probas()#weight=1)
	#code.compute_md5tot_probas_forward()
	#code.compute_md5tot_probas()
	#code.compute_pass_probas()#weight=1)
	print 'original: '+md5_p
	passmd5 = code.guess_pass()
	print 'guessed : '+passmd5
	try:
		decr = code.decrypt(passmd5)
	except ValueError:
		decr = ''
	print 'decrypted : '+ decr
	print 'guessed:    '+ code.guess_string()
print code.pass_p[-1]
print code.clearchars_p[-10:]


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
