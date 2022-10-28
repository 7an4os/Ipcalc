import sys

mask_dec_res=[0,0,0,0]
wild_dec_res=[0,0,0,0]
net_dec_res=[0,0,0,0]
broad_dec_res=[0,0,0,0]

def parse_format(input):
    check=0
    format=0
    res=list()
    mask=""
    input = str(input)
    if "/" in input:
        address_mask = input.split("/")
        mask = address_mask[1]
        check=1
    else:
        check=0
    if "." in mask:
        format=1
    else:
        format=0
    res.append(check)
    res.append(format)
    return res
def parse_data(input): # Проверка самих данных
    input=str(input)
    address_mask=input.split("/")
#    print (address_mask)
    address=address_mask[0]
    mask=address_mask[1]
    octets=address.split(".")
    res=1
    mask_octets=list()
#    print (parse_format(input)[1])
    if (parse_format(input)[1]==1):
        mask_octets=mask.split(".")
    elif(parse_format(input)[1]==0):
        if (mask.isdigit()==True):
            if (int(mask)>32):
                res=11
        else:
            res=10
    mask_bit_res = ""
    if (parse_format(input)[1] == 0):
        for i in range(0, 32):
            if (i < int(mask)):
                mask_bit_res = mask_bit_res + "1"
            else:
                mask_bit_res = mask_bit_res + "0"
    else:
        mask = mask.split(".")
        for i in range(0, len(mask)):
            mask_bit_res += convert_to_bit(int(mask[i]))
    mask_octets=mask_bit_res
## Обработка октетов
    if (len(octets)<4 and len(mask_octets)<4):
        res=20
    else:
        for i in range (0,4):
            if (octets[i]=="" or mask_octets[i]==""):
                return 21
            digit_a=octets[i].isdigit()
            digit_m=mask_octets[i].isdigit()
            if (digit_a==False or digit_m==False):
                return 22
            elif(int(octets[i])>255 or int(mask_octets[i])>255):
                return 23
            elif(int(octets[i])==0 or int(octets[i])==255):
                return 1
            else:
                if (parse_format(input)[1]==1):
                    octet = convert_to_bit(mask_octets[i])
                    mask_check_bit = ""
                    for j in range(0, 8):
                        if (octet[j] == "1"):
                            mask_check_bit += "1"
                        else:
                            break
                    mask_check_dec = convert_to_dec(mask_check_bit)
                    print(mask_check_dec)
                    if (int(mask_octets[i]) != mask_check_dec):
                        return 24

    return res
def convert_to_bit(input): #перевод в биты
    res=[0,0,0,0,0,0,0,0]
    result =""
    i=7
    check=1
    ost=0
    cel=int(input)
    while (check>0):
        ost=cel%2
        #print (ost)
        cel=cel//2
        #print (cel)
        res[i]=ost
        #print (res)
        i = i - 1
        if (cel<=1):
            res[i]=cel
            check=0
        else:
            continue
    for i in range(0,8,1):
        result=result+str(res[i])
    return result
def convert_to_dec(input): #перевод в дес
    res=0
    for i in range(0,len(input),1):
        res=res+(int(input[i])*(2**abs(i-(len(input)-1))))
    return res
def main():
    print("Введите ip и маску в формате X.X.X.X/M")
    # input=input()
    input = "10.191.170.29/24"
    # input="10.191.170.29/55"
    check_format = parse_format(input)
    if (check_format[0] == 0):
        sys.exit("Неверный формат")
    else:
        err_data = parse_data(input)
    # print (err_data)
    if (err_data == 10):
        sys.exit("маска не число либо значение меньше 0")
    elif (err_data == 12):
        sys.exit("выход за пределы допустимого значения")
    elif (err_data == 20):
        sys.exit("недостаточное количество октетов")
    elif (err_data == 21):
        sys.exit("пустой октет")
    elif (err_data == 22):
        sys.exit("в октете не числолибо значение меньше 0")
    elif (err_data == 23):
        sys.exit("выход за пределы допустимого значения")
    elif (err_data == 24):
        sys.exit("значение октета маски неверно")
    addr_mask = input.split("/")
    octets = addr_mask[0].split(".")
    mask = addr_mask[1]
    ##перевод маски в биты
    mask_bit_res = ""
    if (parse_format(input)[1] == 0):
        for i in range(0, 32):
            if (i < int(mask)):
                mask_bit_res = mask_bit_res + "1"
            else:
                mask_bit_res = mask_bit_res + "0"
    else:
        mask = mask.split(".")
        for i in range(0, len(mask)):
            mask_bit_res += convert_to_bit(int(mask[i]))
    ## Кол-во хостов
    quantity_bit = ""
    for i in range(0, 32):
        if (mask_bit_res[i] == "0"):
            quantity_bit += "1"
    hosts = convert_to_dec(quantity_bit) - 1
    ##перевод адреа в биты
    addr_bit = ""
    print(octets)
    for i in range(0, len(octets)):
        addr_bit += convert_to_bit(octets[i])
    ##wildcard
    wildcard = ""
    for i in range(0, 32):
        if (mask_bit_res[i] == "1"):
            wildcard = wildcard + "0"
        else:
            wildcard = wildcard + "1"
    ##Network
    network = ""
    for i in range(0, 32):
        if (mask_bit_res[i] == "1"):
            if (addr_bit[i] == "1"):
                network = network + "1"
            else:
                network = network + "0"
        else:
            network = network + "0"
    ##Broadcast
    broadcast = ""
    broadcast_mask = "111111111111111111111111"
    for i in range(0, 32):
        if (mask_bit_res[i] == 0):
            broadcast = broadcast + addr_bit[i]
        else:
            broadcast = broadcast + "1"
    # Перевод в читаемый вид и обработка
    pos = 0
    for i in range(0, 4):
        mask_octet = ""
        wild_octet = ""
        net_octet = ""
        broad_octet = ""
        for j in range(0, 8):
            mask_octet = mask_octet + mask_bit_res[j + pos]
            wild_octet = wild_octet + wildcard[j + pos]
            net_octet = net_octet + network[j + pos]
            broad_octet = broad_octet + broadcast[j + pos]
        pos = pos + 8
        mask_dec_res[i] = convert_to_dec(mask_octet)
        wild_dec_res[i] = convert_to_dec(wild_octet)
        net_dec_res[i] = convert_to_dec(net_octet)
        broad_dec_res[i] = convert_to_dec(broad_octet)
    print("Mask:      " + str(mask_dec_res[0]) + "." + str(mask_dec_res[1]) + "." + str(mask_dec_res[2]) + "." + str(
        mask_dec_res[3]))
    print("Wildcard:  " + str(wild_dec_res[0]) + "." + str(wild_dec_res[1]) + "." + str(wild_dec_res[2]) + "." + str(
        wild_dec_res[3]))
    print("Network:   " + str(net_dec_res[0]) + "." + str(net_dec_res[1]) + "." + str(net_dec_res[2]) + "." + str(
        net_dec_res[3]))
    print("Broadcast: " + str(broad_dec_res[0]) + "." + str(broad_dec_res[1]) + "." + str(broad_dec_res[2]) + "." + str(
        broad_dec_res[3]))
    print("hostMin:   " + str(net_dec_res[0]) + "." + str(net_dec_res[1]) + "." + str(net_dec_res[2]) + "." + str(
        net_dec_res[3] + 1))
    print("hostMax:   " + str(broad_dec_res[0]) + "." + str(broad_dec_res[1]) + "." + str(broad_dec_res[2]) + "." + str(
        broad_dec_res[3] - 1))
    print("Hosts/Net: " + str(hosts))
    print("Prefered gateway " + str(net_dec_res[0]) + "." + str(net_dec_res[1]) + "." + str(net_dec_res[2]) + "." + str(
        net_dec_res[3] + 1))

if __name__ == '__main__':
    sys.exit(main())


