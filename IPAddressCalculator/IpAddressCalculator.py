# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 07:52:47 2018

@author: gmcbrid
"""

import re

def getValidHostRange(userIPAddress, userSubnetMask):
    pass

def getRequiredSubnetMask(reqNumHosts):
    hostBits = 1
    numOfHosts = 0
    initialOneBits = 32
    SubnetMaskBinary = []
    newSubnetMaskBinary = []
    SubnetMaskBinaryStr = ""
    decimalMaskList = []
    validSubnetMasks = {"11111111": 255 , "11111110": 254 , "11111100": 252 , "11111000": 248 , "11110000": 240 , "11100000": 224 , "11000000": 192 , "10000000": 128 , "00000000": 0}

    for num in range(1,32):
        numOfHosts = 2**hostBits
        
        if numOfHosts >= int(reqNumHosts):
            break
        
        hostBits += 1
    
    newOneBits = initialOneBits - hostBits
    
    count = 1
    while count <=  newOneBits:
        SubnetMaskBinary.append("1")
        
        count += 1
    
    count = 1
    while count <= hostBits:
        SubnetMaskBinary.append("0")
        count += 1
    
    SubnetMaskBinaryStr = "".join(SubnetMaskBinary)

    newSubnetMaskBinary.append(SubnetMaskBinaryStr[0:8])
    newSubnetMaskBinary.append(SubnetMaskBinaryStr[8:16])
    newSubnetMaskBinary.append(SubnetMaskBinaryStr[16:24])
    newSubnetMaskBinary.append(SubnetMaskBinaryStr[24:32])

    for octet in newSubnetMaskBinary:

        if octet in validSubnetMasks:
            decimalMaskList.append(validSubnetMasks.get(octet))
    
    subnetString = [str(decimalMaskList[x]) for x in range(len(decimalMaskList))]
     
    return subnetString
    

def getBroadcastAdress(ipAddress, subnetMask):
    decimalValue = [128,64,32,16,8,4,2,1]
    
    maskList = subnetMask.split(".")
    ipList = ipAddress.split(".")
    maskList = [int(maskList[x]) for x in range(len(maskList))]
    ipList = [int(ipList[x]) for x in range(len(ipList))]    
    
    maskBinary = []
    octetCareBits = 0
    
    for octet in maskList:
        
        maskBinary = convertToBinary(octet)     
        if 0 in maskBinary: 
            break
        
        else:
            octetCareBits += 1
            
    ipBinary = convertToBinary(ipList[octetCareBits])
    
    careBitsCount = 0
    broadcastAddressOctetDecimal = 0 

    for bit in ipBinary:
        if maskBinary[careBitsCount] == 1:
            broadcastAddressOctetDecimal = broadcastAddressOctetDecimal + (ipBinary[careBitsCount] * decimalValue[careBitsCount])
        elif maskBinary[careBitsCount] == 0:
            broadcastAddressOctetDecimal = broadcastAddressOctetDecimal + (1 * decimalValue[careBitsCount])
        
        careBitsCount = careBitsCount + 1
    
    ipList[octetCareBits] = broadcastAddressOctetDecimal
    while octetCareBits+1 <= 3:
        ipList[octetCareBits+1] = 255
        octetCareBits = octetCareBits + 1
    ipString = [str(ipList[x]) for x in range(len(ipList))]
    
    return ".".join(ipString)

  
def getNetworkAdress(ipAddress, subnetMask):
    decimalValue = [128,64,32,16,8,4,2,1]
    
    maskList = subnetMask.split(".")
    ipList = ipAddress.split(".")
    maskList = [int(maskList[x]) for x in range(len(maskList))]
    ipList = [int(ipList[x]) for x in range(len(ipList))]
    
    maskBinary = []
    octetCareBits = 0
    
    #convert each octet of subnet mask to binary and determine the "care bits" octet where subnetting is occuring
    for octet in maskList:
        
        maskBinary = convertToBinary(octet)     
        if 0 in maskBinary:
            
            break
        else:
            octetCareBits += 1
    
    #converts "care bits" octet of IP Address to binary based on "care bits" octet above.
    ipBinary = convertToBinary(ipList[octetCareBits])
    
    careBitsCount = 0
    networkAddressOctetDecimal = 0 
    
    #calculates network address by checking "care bits" in subnet mask, and if it is 1, it adds it to the decimal value.
    for bit in ipBinary:
        if maskBinary[careBitsCount] == 1:
            networkAddressOctetDecimal = networkAddressOctetDecimal + (ipBinary[careBitsCount] * decimalValue[careBitsCount])
        elif maskBinary[careBitsCount] == 0:
            break
        
        careBitsCount = careBitsCount + 1
    
    ipList[octetCareBits] = networkAddressOctetDecimal
    
    #Makes the octets following the network addrress octet 0
    while octetCareBits+1 <= 3:
        ipList[octetCareBits+1] = 0
        octetCareBits = octetCareBits + 1
    
    #converts the integer version of the Network Address back to a string to allow the ".join" command
    ipString = [str(ipList[x]) for x in range(len(ipList))]
    
    return ".".join(ipString)
    
    
def isValidIPAdress(ipAddress):
    pattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    isValidIP = re.fullmatch(pattern, ipAddress)
    ipList = ipAddress.split(".")
    validIP = False
    
    #isValidIP will be None if Regex search does not find a full match and immediately classify the IP Address as incorrect.
    #If isValidIP is a value, it will check if there are no more than 4 octets
    #If 4 octets, converts octets to integers and checks that IP address is in each octet is between 0 and 255
    if isValidIP == None:
        
        return False
    elif len(ipList) > 4: 

        return False
    
    else:
        
        ipList = [int(ipList[x]) for x in range(len(ipList))]
        for octetIP in ipList:
                        
            if octetIP in range(0,255):
                validIP = True
               
            else:
                return False
            
    #Returns True if all above are true. Returns False otherwise.    
    if validIP == True:
        return True
    else:
        return False
    
def isValidSubnetMask(subnetMask):
    pattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    isValidMask = re.fullmatch(pattern, subnetMask)
    validSubnetMasks = [255,254,252,248,240,224,192,128,0]
    maskList = subnetMask.split(".")
    octetBinaryList = []
    cidrNotation = 0
    #validMask = False
    
    #validMask will be None if Regex search does not find a full match and immediately classify the subnet mask as incorrect.
    #If validMask is a value, it will check if there are no more than 4 octets
    #If 4 octets, converts octets to integers and checks that subnet mask is in each octet is in validSubnetMasks, a list of -
    #valid decimal values for an octet in a subnet mask
    if isValidMask == None:
        
        return False
    
    elif len(maskList) > 4: 
        
        return False
    
    else:
        
        maskList = [int(maskList[x]) for x in range(len(maskList))]
            
        for octet in maskList:
            if octet not in validSubnetMasks:
                return False
            else:
                octetBinaryList = octetBinaryList + convertToBinary(octet)
            
                
                for bit in octetBinaryList:
                    if bit == 1:
                        cidrNotation = cidrNotation + 1
                    elif bit == 0:
                        break
                
        cidrNotation = octetBinaryList.index(0)
        global networkPortionList
        global hostPortionList
        networkPortionList = octetBinaryList[:cidrNotation]
        hostPortionList = octetBinaryList[cidrNotation::]

        
        if 1 in hostPortionList:
            return False
        else:
            return True

def subnetMaskToBinary(subnetMask):
    maskList = subnetMask.split(".")
    binaryMaskList = []
    validSubnetMasks = {255: "11111111",254: "11111110",252: "11111100",248: "11111000",240: "11110000",224: "11100000",192: "11000000",128: "10000000",0: "00000000"}
    
    #First check if it's a valid subnet mask by calling isValidSubnetMask(subnetMask).
    #If a valid subnet mask, check for decimal value in validSubnetMasks list and place binary string in binaryMaskList.
    if isValidSubnetMask(subnetMask):
        for octet in maskList:
            
            if int(octet) in validSubnetMasks:
                binaryMaskList.append(validSubnetMasks.get(int(octet)))
            
    else:
        return ValueError

    #Returns a list - with each element being a string of binary values.
    return binaryMaskList
    
def convertToBinary(address):
    
    binary_address = [0,0,0,0,0,0,0,0]
    
    #Iterates over the length of an octet (8 bits), if decimal 0, return bits of all zeros.
    #If a value above 0, perform decimal to binary conversion.
    for bit in range(len(binary_address)):
        
        if address == 0:
            binary_address[::-1]
        else:
            remainder = address%2
            address = address//2
            
            binary_address[bit] = remainder
            
    #Swops the lits of bits around to swop around LSB and MSB 
    return binary_address[::-1]
            
def main():
    
    print("IP ADDRESS CALCULATOR")
    print("Enter 1, 2, 3 or 4 for the option should would like to perform:")
    print("1. Get the Network Address and Broadcast address for an IP Address/Subnet Mask pair")
    print("2. Get the valid host range for an IP Address and subnet mask")
    print("3. Calculate Subnet Mask for desired number of host addresses")
    print("4. Convert subnet mask to binary")
    userSelection = input("Option: ").strip()

    if userSelection == "1":
        
        try:    
            userIPAddress = input("Please enter the IP Address: ")
            
            if isValidIPAdress(userIPAddress):
                userSubnetMask = input("Please enter the Subnet Mask: ")
                if isValidSubnetMask(userSubnetMask):
                    print("The Network Address is: ", getNetworkAdress(userIPAddress, userSubnetMask))
                    print("The Broadcast Address is: ", getBroadcastAdress(userIPAddress, userSubnetMask))
                    
                else:
                    print("INVALID")
                    raise ValueError
                

            else:
                print("INVALID")
                raise ValueError
                
        except:
            print("Not a valid Address.") 
        
    elif userSelection == "2":
        try:    
            userIPAddress = input("Please enter the IP Address: ")
            userSubnetMask = input("Please enter the Subnet Mask: ")
            print("Valid host range is: " , getValidHostRange(userIPAddress, userSubnetMask))
        except:
            pass
            
    elif userSelection == "3":
        #try:    
        userHosts = input("Please enter the number of hosts addresses you require: ")

        print("You will need a subnet mask of:" , ".".join(getRequiredSubnetMask(userHosts)))
            
        
        #except:
          #  print("Error occured")
    elif userSelection == "4":
        try:    

            userSubnetMask = input("Please enter the Subnet Mask: ")
            maskList = userSubnetMask.split(".")
            
            count = 0 
            
            for octet in subnetMaskToBinary(userSubnetMask):
                print(maskList[count].ljust(3), "-", octet)
                count += 1
               
                
        except:
            print("Error occured")
    else:
        pass
    
    #print(getNetworkAndBroadcastAdress("192.168.1.50", "255.255.255.224"))
    
    
if __name__ == "__main__":
    main()
