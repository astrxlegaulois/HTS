#!/usr/bin/python
# Solution du challenge https://www.hackthissite.org/missions/prog/3/

# ----Imports
import md5
import array
# ----Fonctions originales traduites en python


def evalCrossTotal(strMD5):
	"""
	Sums the hexa values of the input string
	"""
	intTotal = 0
	for v in strMD5:
		if(ord(v)>ord('9')):
			intTotal+=ord(v)-ord('a')+10
			# print v,ord(v)-ord('a')+10
		else:
			intTotal+=ord(v)-ord('0')
			# print v,ord(v)-ord('0')
	return intTotal

def encryptString(strString, passw=None, md5=None):
    """
    Encrypts a string
    """
    if passw is not None:
        strPasswordMD5 = md5.new(passw).hexdigest() #or use digest() ??
    elif md5 is not None:
        strPasswordMD5 = md5
    else:
        raise IOError('password or md5 needed')
    print "strPasswordMD5",strPasswordMD5
    intMD5Total = evalCrossTotal(strPasswordMD5)
    print "new intMD5Total",intMD5Total
    arrEncryptedValues=[]
    intStrlen = len(strString)
    str_list = []
    for i in range(intStrlen):
        if strString[i] == 'n' and str_list[-1] == '\\':
            str_list[-1] = '\n'
        else:
            str_list.append(strString[i])
    for i in range(len(str_list)):
        print "i: ",i
        print "char to encode: ",ord(str_list[i])
        print "passMd5contrib: ",int(strPasswordMD5[i%32],16)
        arrEncryptedValues.append(ord(str_list[i])+int(strPasswordMD5[i%32],16)-int(intMD5Total))
        print "left part: ",md5.new(''.join(str_list[0:i+1])).hexdigest()[0:16]
        print "right part: ",md5.new(str(intMD5Total)).hexdigest()[0:16]
        intMD5Total = evalCrossTotal(md5.new(''.join(str_list[0:i+1])).hexdigest()[0:16] + md5.new(str(intMD5Total)).hexdigest()[0:16])
        print "new intMD5Total: ",intMD5Total
    return arrEncryptedValues

# ----Fonctions de decryptage

def getMd5Tables():
    """
    Returns a table of the 16 md5sums of the low case hexa numbers
    """
    ans=[]
    for i in range(16):
        ans.append(md5.new(str(i)).hexdigest())
    return ans

def getPotentialClearCharsAtPosition(position,chars=[str(i) for i in range(10)]+[chr(i) for i in range(ord("A"),ord("Z")+1)]):
    """
    Returns all the possible unencrypted chars of the string at the specified position
    """
    ans=[]
    if position % 20 in [3, 7, 11, 15]:
        ans.append("-")
    elif position%20 == 8 :
        ans.append("O")
    elif position%20 == 9 :
        ans.append("E")
    elif position%20 == 10 :
        ans.append("M")
    elif position%20 == 17 :
        ans.append(".")
    elif position%20 == 16 or position%20 == 18:
        ans.append("1")
    elif position%20 == 19 :
        ans.append("\n")
    else:
        ans += chars
    return ans

def generateClearCharsList(length=100,chars=[str(i) for i in range(10)]+[chr(i) for i in range(ord("A"),ord("Z")+1)]):
    """
    Returns the initial list of potential characters
    """
    ans=[]
    for i in range(length):
        ans.append(getPotentialClearCharsAtPosition(i,chars=chars))
    return ans

def generatePasswordMD5():
    """
    returns the initial list of potential hex values of the md5Password
    """
    ans=[]
    for i in range(32):
        ans.append([])
        for j in range(16):
            ans[-1].append(hex(j)[2])
    return ans

def generateMD5Total(length=100, init_val=None, dist_max=240):
    """
    returns the initial list of potential md5Total
    """
    if init_val is None:
        ans = [i for i in range(481) if abs(240-i)<=dist_max]
    else:
        ans = [[init_val]]
    for i in range(length-1):
        ans.append([i for i in range(481) if abs(240-i)<=dist_max])
    return ans

def refinePotentialClearChars(potentialClearChars,potPasswordMD5,potMD5Total,encryptedText,position):
    """
    Removes all impossible values for potentialClearChars given the potMD5Total hypothesis, the available potPasswordMD5 values and the encrypted value of the char
    """
    for j in [i for i in potentialClearChars[position]]:
        try:
            for k in potPasswordMD5[position%32]:
                for t in potMD5Total[position]:
                    if ord(j)==int(encryptedText[position])-int(k,16)+t:
                        raise Exception('found')
            potentialClearChars[position].remove(j)
        except Exception as e:
            if e.args[0] == 'found':
                pass
            else:
                raise
    if not potentialClearChars[position]:
           raise Exception('Bachata')

def refinePotentialPasswordMD5(potentialClearChars,potPasswordMD5,potMD5Total,encryptedText,position):
    """
    Removes all impossible values for potPasswordMD5 given the potentialClearChars, the potMD5Total hypothesis, and the encrypted value of the char
    """
    for j in [i for i in potPasswordMD5[position%32]]:
        try:
            for k in potentialClearChars[position]:
                for t in potMD5Total[position]:
                    if int(j,16)==int(encryptedText[position])-ord(k)+t:
                        raise Exception('found')
            potPasswordMD5[position%32].remove(j)
        except Exception as e:
            if e.args[0] == 'found':
                pass
            else:
                raise
    if not potPasswordMD5[position%32]:
           raise Exception('Bachata')

def gen_begin_strings(potentialClearChars,pos_max):
    """
    Generates all possible beginning of string until position pos_max, given the potential char list
    """
    ans = ['']
    for i in range(pos_max):
        temp_ans = []
        for j in potentialClearChars[i]:
            for k in ans:
                temp_ans.append(k + j)
                if len(temp_ans)>10**7:
                    raise Exception('Ta Ram va me remercier')
        ans = temp_ans
    return ans

def forward_refinePotentialMD5Total(potentialClearChars,potPasswordMD5,potMD5Total,encryptedText,position):
    """
    Removes all impossible values at given position for potMD5Total given the potentialClearChars, the potPasswordMD5, and the encrypted values
    """
    if position>=len(potMD5Total):
        return None
    init_set = set(potMD5Total[position])
    val_set = set()
    for s in gen_begin_strings(potentialClearChars,position):
        for t in potMD5Total[position-1]:
            value = evalCrossTotal(md5.new(s).hexdigest()[0:16] + md5.new(str(t)).hexdigest()[0:16])
            val_set.add(value)
            if init_set<=val_set:
                return None
    final_set = init_set & val_set
    potMD5Total[position] = list(final_set)
    if not potMD5Total[position]:
           raise Exception('Bachata')

def backward_refinePotentialMD5Total(potentialClearChars,potPasswordMD5,potMD5Total,encryptedText,position):
    """
    Backwards removal of all impossible values at given position for potMD5Total given the potentialClearChars, the potPasswordMD5, and the encrypted values
    """
    if position+1>=len(potMD5Total):
        return None
    for j in [i for i in potMD5Total[position]]:
        try:
            for k in potentialClearChars[position+1]:
                for p in potPasswordMD5[(position+1)%32]:
                    for t in potMD5Total[position+1]:
                        if int(p,16)==int(encryptedText[position+1])-ord(k)+t:
                            raise Exception('found')
            potMD5Total[position].remove(j)
        except Exception as e:
            if e.args[0] == 'found':
                pass
            else:
                raise
    if not potMD5Total[position]:
           raise Exception('Bachata')

def refine(args, position, way='forward'):
    if way == 'forward':
       refinePotentialClearChars(*args, position=position)
       refinePotentialPasswordMD5(*args, position=position)
       forward_refinePotentialMD5Total(*args, position=position+1)
    else:
       backward_refinePotentialMD5Total(*args, position=position)
       refinePotentialClearChars(*args, position=position)
       refinePotentialPasswordMD5(*args, position=position)

def decrypt(encryptedString):
    """
    Bruteforce decryption of the String
    The md5 of the password will be recovered in the process
    """
    #initialisation of the tables


    #try most probable values of potMD5Total first
    for j in [240+int((i+1)/2)*(-1)**i for i in range(481)]:# + list(reversed(range(225))): #[240+int((i+1)/2)*(-1)**i for i in range(480) if 0<=240+int((i+1)/2)*(-1)**i<=255]
        try:
            potentialClearChars=generateClearCharsList(len(encryptedString))
            potPasswordMD5=generatePasswordMD5()
            potMD5Total=generateMD5Total(len(encryptedString),init_val=j)
            print "potMD5Total:",j
            for position in range(len(encryptedString)):
                print "position:", position
                for i in range(position):
                    refine([potentialClearChars,potPasswordMD5,potMD5Total,encryptedString],position=position)
                #if position%20 in [3,7,8,9,10,11,16,17,18,19]:
                #    for i in list(reversed(range(position-1))):
                #        refine([potentialClearChars,potPasswordMD5,potMD5Total,encryptedString],position=position,way='backward')
                print 'Potential chars: '+str(potentialClearChars[position])
            found_possib = 1
            for position in range(len(encryptedString)):
                found_possib *= len(potentialClearChars[position])
            if found_possib == 1:
                s = gen_begin_strings(potentialClearChars,len(potentialClearChars))
                print 'FOUND for init_value = '+str(j)+' : '+s
        except Exception as e:
            if e.args[0] == 'Bachata':
                print '0 possibilities for init_val = '+str(j)
            else:
                raise
    return 'finished without finding anything?'

def probas_output_sample(output):
    ans = {}
    for i in range(len(output)):
        if output[i] not in ans.keys():
            ans[output[i]] = 1
        else:
            ans[output[i]] +=1
    print ans
    return ans

# ----Main


class CodeToDecrypt(object):
    def __init__(self, dist_max=240,chars=[str(i) for i in range(10)]+[chr(i) for i in range(ord("A"),ord("Z")+1)],code=[-166,-153,-114,-191,-151,-185,-156,-156,-159,-151,-130,-180,-164,-166,-169,-152,-162,-163,-132,-238,-114,-190,-136,-195,-191,-167,-177,-204,-131,-185,-118,-183,-106,-197,-159,-192,-188,-194,-168,-188,-137,-85,-172,-187,-125,-189,-187,-165,-132,-118,-163,-208,-164,-151,-194,-146,-228,-160,-178,-243,-119,-142,-163,-212,-148,-72,-169,-137,-129,-202,-172,-218,-176,-113,-220,-167,-182,-212,-175,-221,-134,-143,-130,-116,-125,-128,-149,-184,-100,-184,-162,-187,-153,-132,-172,-176,-204,-186,-188,-204]):
        self.code = code
        self.dist_max = dist_max
        self.chars = chars
        self.pot_char = generateClearCharsList(len(code),chars=chars)
        self.pot_pass = generatePasswordMD5()
        self.remaining_init_values = [240+int((i+1)/2)*(-1)**i for i in range(481)]
        self.init_value = self.remaining_init_values.pop(0)
        self.pot_total = generateMD5Total(len(self.code),init_val=self.init_value,dist_max=self.dist_max)

    def nb_possibilities(self,what=None):
        ans = 1
        if what is None:
            for position in range(len(self.pot_char)):
                ans *= len(self.pot_char[position])
        elif what is 'pass':
            for position in range(32):
                ans *= len(self.pot_pass[position])
        elif what is 'total':
            for position in range(len(self.pot_total)):
                ans *= len(self.pot_total[position])
        return ans


    def next_init_value(self):
        self.init_value = self.remaining_init_values.pop(0)
        self.pot_total = generateMD5Total(len(self.code),init_val=self.init_value,dist_max=self.dist_max)
        self.pot_char = generateClearCharsList(len(self.code),chars=self.chars)
        self.pot_pass = generatePasswordMD5()

    def step(self):
        try:
            potentialClearChars=self.pot_char
            potPasswordMD5=self.pot_pass
            potMD5Total=self.pot_total
            encryptedString = self.code
            print "potMD5Total:",self.init_value
            for position in range(len(encryptedString)):
                print "position:", position
                for i in range(position+1):
                    refine([potentialClearChars,potPasswordMD5,potMD5Total,encryptedString],position=position)
                if True: #position%20 in [3,7,8,9,10,11,16,17,18,19]:
                    for i in list(reversed(range(position))):
                        refine([potentialClearChars,potPasswordMD5,potMD5Total,encryptedString],position=position,way='backward')
                print 'Potential chars: '+str(potentialClearChars[position])
                print 'Potential Pass hex: '+str(potPasswordMD5[position%32])
                print '# Potential MD5total: '+str(len(potMD5Total[position]))
            found_possib = 1
            for position in range(len(encryptedString)):
                found_possib *= len(potentialClearChars[position])
            if found_possib == 1:
                s = gen_begin_strings(potentialClearChars,len(potentialClearChars))
                print 'FOUND for init_value = '+str(self.init_value)+' : '+''.join(s)
                print 'Passmd5: '+''.join([i[0] for i in self.pot_pass])
        except Exception as e:
            if e.args[0] == 'Bachata':
                print '0 possibilities for init_val = '+str(self.init_value)
            else:
                raise
        return 'finished without finding anything?'

    def decrypt(self,steps=None):
        if steps is None:
            steps = len(self.remaining_init_values)+1
        for i in range(min(steps,len(self.remaining_init_values))+1):
            self.step()
            if self.nb_possibilities()*self.nb_possibilities('pass')*self.nb_possibilities('total') > 0:
                print self.nb_possibilities(), self.nb_possibilities('pass'), self.nb_possibilities('total')
                print 'FOUND '+str(self.nb_possibilities())+' possibilities with init_md5total='+str(self.init_value)
                print 'first: '+''.join([i[0] for i in self.pot_char])
                break
            if self.remaining_init_values:
                self.next_init_value()


def test():
    test_str = '0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'+'0Z0-0Z0-OEM-0Z0-1.1\n'
    passw = 'leanaperd'
    enc = encryptString(test_str,passw)
    code = CodeToDecrypt(chars=['0','A','Z'],code=enc,dist_max=100)
    #code = CodeToDecrypt(code=enc,dist_max=40)
    code.decrypt()
    return code

if __name__ == '__main__':
    #code = [-166,-153,-114,-191,-151,-185,-156,-156,-159,-151,-130,-180,-164,-166,-169,-152,-162,-163,-132,-238,-114,-190,-136,-195,-191,-167,-177,-204,-131,-185,-118,-183,-106,-197,-159,-192,-188,-194,-168,-188,-137,-85,-172,-187,-125,-189,-187,-165,-132,-118,-163,-208,-164,-151,-194,-146,-228,-160,-178,-243,-119,-142,-163,-212,-148,-72,-169,-137,-129,-202,-172,-218,-176,-113,-220,-167,-182,-212,-175,-221,-134,-143,-130,-116,-125,-128,-149,-184,-100,-184,-162,-187,-153,-132,-172,-176,-204,-186,-188,-204]
    #code_obj = CodeToDecrypt(code=code,dist_max=60)
    #code_obj.decrypt()

    #test()
    with open('output_sample','r') as f:
        output = f.read()
    probas_output_sample(output)
    print sum([ord(j) for j in output])/15
    print sum([ord(j) for j in output])/15
    print sum([ord(j) for j in output])/15
    with open('output_sample','r') as f:
        output = f.readlines()
    for i in output:
        print sum([ord(j) for j in i])

    ll = [str(i) for i in range(10)]+[chr(i) for i in range(ord('A'),ord('Z')+1)]
    lll = range(ord('0'),ord('9')+1)+range(ord('A'),ord('Z')+1)
    exp = sum(lll)/len(lll)
    offset = ord('O')+ord('E')+ord('M')+4*ord('-')+2*ord('1')+ord('\n')
    print offset + 10*exp

