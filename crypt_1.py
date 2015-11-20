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

def encryptString(strString, strPassword):
    """
    Encrypts a string
    """
    strPasswordMD5 = md5.new(strPassword).hexdigest() #or use digest() ??
    print "strPasswordMD5",strPasswordMD5
    intMD5Total = evalCrossTotal(strPasswordMD5)
    print "new intMD5Total",intMD5Total
    arrEncryptedValues=[]
    intStrlen = len(strString)
    for i in range(0,intStrlen):
        print "i: ",i
        print "char to encode: ",ord(strString[i:i+1])
        print "passMd5contrib: ",int(strPasswordMD5[i%32],16)
        arrEncryptedValues.append(ord(strString[i:i+1])+int(strPasswordMD5[i%32],16)-int(intMD5Total))
        print "left part: ",md5.new(strString[0:i+1]).hexdigest()[0:16]
        print "right part: ",md5.new(str(intMD5Total)).hexdigest()[0:16]
        intMD5Total = evalCrossTotal(md5.new(strString[0:i+1]).hexdigest()[0:16] + md5.new(str(intMD5Total)).hexdigest()[0:16])
        print "new intMD5Total: ",intMD5Total
    return arrEncryptedValues

# ----Fonctions de decryptage

# ----Main
