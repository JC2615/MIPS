registers = ["0000","0000","DD","0000","158","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000"]
mem = ["0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000","0000"]
pc = 0

#Decimal to binary function
def dToB(dec):
    #Instantiate a list to store the binary numbers
    binary = []

    #Sets up quotient and remainder to use
    quotient = 0
    base2 = 0

    #Divides by 2 until quotient equals 0 and adds the remainders to the binary list
    while (True):
        quotient = dec // 2
        base2 = dec % 2
        dec = quotient
        binary.append(str(base2))
        if quotient==0:
            break
    
    #Reverses list because the remainders have to be written in reverse order from when they were found to be correct
    binary.reverse()

    if len(binary) < 4:
        for _ in range(4 - len(binary)):
            binary.insert(0, "0")

    #Prints the binary representation
    s = ""
    
    return s.join(binary)

#Binary to decimal function
def bToD(binary):
    #Makes each bit an item in a list in order to multiply its position by its respective power of 2
    binary = str(binary)
    binary = [int(i) for i in binary]

    #Reverses list of bits because it makes it easier for the upcoming loop
    binary.reverse()

    #Sets up the decimal number that will be printed out
    decimal = 0

    #Loops over every bit and multiplies the bit by its respective power of two then adds the product to the decimal variable
    for i in range(len(binary)):
        decimal += (binary[i] * (2**i))

    #Prints the decimal representation of the entered binary number
    return decimal

def hToB(hexadecimal):
    hexadecimal = [i.upper() for i in hexadecimal]

    binary = ""
    conversion = {"0":dToB(0), "1":dToB(1), "2":dToB(2), "3":dToB(3), "4":dToB(4), "5": dToB(5), "6":dToB(6), "7":dToB(7), "8":dToB(8), "9":dToB(9), "A":dToB(10), "B":dToB(11), "C":dToB(12), "D":dToB(13), "E":dToB(14), "F":dToB(15)}
    for num in hexadecimal:
        binary += str(conversion[num])

    return binary

def bToH(binary):
    hexadecimal = ""
    four = ""

    conversion = {"0":"0", "1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9", "10":"A", "11":"B", "12":"C", "13":"D", "14":"E", "15":"F"}
    for i in range(len(binary)-1,-1,-1):
        four += binary[i]
        if len(four) == 4:
            hexadecimal += conversion[str(bToD(four[::-1]))]
            four = ""
    
    if four:
        hexadecimal += conversion[str(bToD(four[::-1]))]

    return hexadecimal[::-1]

def i_format(instruction):
    i_instructions = {35:"lw", 43:"sw", 4:"beq", 5:"bne", 8:"addi"}
    op = instruction[0:6]
    rs = bToD(instruction[6:11])
    rd = bToD(instruction[11:16])
    address = instruction[16:]
    global pc

    if i_instructions[bToD(op)] == "lw":
        string = f"{i_instructions[bToD(op)]} ${rd},  {bToD(address)}(${rs})"
        registers[rd] = mem[bToD(address) + bToD(hToB(registers[rs]))]
    elif i_instructions[bToD(op)] == "sw":
        string = f"{i_instructions[bToD(op)]} ${rd},  {bToD(address)}(${rs})"
        mem[bToD(address) + bToD(hToB(registers[rs]))] = registers[rd]
    elif i_instructions[bToD(op)] == "addi":
        if address[0] == "1":
            tc = ""
            for num in address:
                if num == "1":
                    tc += "0"
                else:
                    tc += "1"
            tc = bToD(tc) + 1
            address = dToB(tc)

        string = f"{i_instructions[bToD(op)]} ${rd}, ${rs}, {bToD(address)}"
        registers[rd] = bToH(dToB(bToD(address) + bToD(hToB(registers[rs]))))
    elif i_instructions[bToD(op)] == "beq":
        string = f"{i_instructions[bToD(op)]} ${rd}, ${rs}, {bToD(address)}"
        if rd == rs:
            pc += bToD(address)
    elif i_instructions[bToD(op)] == "bne":
        string = f"{i_instructions[bToD(op)]} ${rd}, ${rs}, {bToD(address)}"
        if rd != rs:
            pc += bToD(address)
    else:
        print("Invalid instruction.")
            
    print(string)

def r_format(instruction):
    r_instructions = {36:"and", 37:"or", 32:"add", 34:"sub"}
    rs = bToD(instruction[6:11])
    rt = bToD(instruction[11:16])
    rd = bToD(instruction[16:21])
    funct = bToD(instruction[21:])

    string = f"{r_instructions[funct]} ${rd}, ${rs}, ${rt}"

    if r_instructions[funct] == "add":
        registers[rd] = bToH(dToB(bToD(hToB(registers[rs])) + bToD(hToB(registers[rt]))))
    elif r_instructions[funct] == "sub":
        registers[rd] = bToH(dToB(bToD(hToB(registers[rs])) - bToD(hToB(registers[rt]))))
    elif r_instructions[funct] == "or":
        first = list(hToB(registers[rs]))
        second = list(hToB(registers[rt]))
        third = []

        if len(second) > len(first):
            for i in range(len(second)-len(first)):
                first.append("0")
            first.reverse()
        elif len(first) > len(second):
            for i in range(len(first)-len(second)):
                second.append("0")
            second.reverse()

        for i in range(len(first)):
            if (first[i] == "1" and second[i] == "1") or (first[i] == "1" and second[i] == "0") or (first[i] == "0" and second[i] == "1"):
                third.append("1")
            else:
                third.append("0")
        
        registers[rd] = bToH("".join(third))
    elif r_instructions[funct] == "and":
        first = list(hToB(registers[rs]))
        second = list(hToB(registers[rt]))
        third = []
        print(len(first), first, "  ", second, len(second))
        if len(second) > len(first):
            for i in range(len(second)-len(first)):
                first.append("0")
            first.reverse()
        elif len(first) > len(second):
            for i in range(len(first)-len(second)):
                second.append("0")
            second.reverse()
        print(first, second)
        for i in range(len(first)):
            third.append(str( int(first[i]) * int(second[i]) ))
        
        registers[rd] = bToH("".join(third))
    else:
        print("Invalid instruction.")
            
    print(string)

def main():
    global pc

    while(True):
        instruction = input("Enter a hexadecimal intruction: ")
        if instruction == "stop":
            break
        instruction = hToB(instruction)
        if instruction[0:4] == "0000":
            r_format(instruction)
            pc += 4
        else:
            i_format(instruction)
            pc += 4
        print(f"\nPC: {bToH(dToB(pc))}\n")
        print("Registers:")
        for i in range(len(registers)):
            if i != 26 and i != 27:
                print(f"r{i}: {registers[i]}")
        
main()
