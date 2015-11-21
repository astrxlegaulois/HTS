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
    for i in range(intStrlen):
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

def getMd5Tables():
    """
    Returns a table of the 16 md5sums of the low case hexa numbers
    """
    ans=[]
    for i in range(16):
        ans.append(md5.new(str(i)).hexdigest())
    return ans

def getPotentialClearCharsAtPosition(position):
    """
    Returns all the possible unencrypted chars of the string at the specified position
    """
    ans=[]
    if ((position % 20 == 3 or position % 20 == 7) or position % 20 == 11):
        ans.append("-")
    elif position%20 == 6 :
        ans.append("O")
    elif position%20 == 7 :
        ans.append("E")
    elif position%20 == 8 :
        ans.append("M")
    elif position%20 == 17 :
        ans.append(".")
    elif position%20 == 16 or position%20 == 18:
        ans.append("1")
    elif position%20 == 19 :
        ans.append("\n")
    else:
        for i in range(0,10):
            ans.append(str(i))
        for i in range(ord("A"),ord("Z")+1):
            ans.append(chr(i))
    return ans

def generateClearCharsList(length=100):
    """
    Returns the initial list of potential characters
    """
    ans=[]
    for i in range(length):
        ans.append(getPotentialClearCharsAtPosition(i))
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

def refinePotentialClearChars(potentialClearChars,potPasswordMD5,potMD5Total,encryptedText,position):
    """
    Removes all impossible values for potentialClearChars given the potMD5Total hypothesis, the available potPasswordMD5 values and the encrypted value of the char
    """
    for j in [i for i in potentialClearChars[position]]:
        found=False
        for k in potPasswordMD5[position%32]:
            if ord(j)==encryptedText[position]-int(k,16)+potMD5Total:
                found=True
                break
        if not found:
            potentialClearChars[position].remove(j)


def refinePotentialPasswordMD5(potentialClearChars,potPasswordMD5,potMD5Total,encryptedText,position):
    """
    Removes all impossible values for potPasswordMD5 given the potentialClearChars, the potMD5Total hypothesis, and the encrypted value of the char
    """
    for j in [i for i in potPasswordMD5[position%32]]:
        found=False
        for k in potentialClearChars[position]:
            if int(j,16)==encryptedText[position]-ord(k)+potMD5Total:
                found=True
                break
        if not found:
            potPasswordMD5[position%32].remove(j)
    

def decrypt(encryptedString):
    """
    Bruteforce decryption of the String
    The md5 of the password will be recovered in the process
    """
    #initialisation of the tables


    #try most probable values of potMD5Total first
    for j in [240+int((i+1)/2)*(-1)**i for i in range(31)] + list(reversed(range(225))): #[240+int((i+1)/2)*(-1)**i for i in range(480) if 0<=240+int((i+1)/2)*(-1)**i<=255]
        potentialClearChars=generateClearCharsList(len(encryptedString))
        potPasswordMD5=generatePasswordMD5()
        print "potMD5Total:",potMD5Total
        for position in range(len(encryptedString)):
            print "position:", position
            refinePotentialClearChars(potentialClearChars,potPasswordMD5,potMD5Total,encryptedString,position)
            if not potentialClearChars[position]:
                break
            refinePotentialPasswordMD5(potentialClearChars,potPasswordMD5,potMD5Total,encryptedString,position)
            if not potPasswordMD5[position%32]:
                break
            potMD5Total=iterate #!!!!!!!!!!!!!!!!

    
    
    return strString
# ----Main
