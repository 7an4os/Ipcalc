from main import parse_format
from main import parse_data
from main import convert_to_bit
from main import convert_to_dec

input_parse_format=["10.191.170.29/22","10.191.170.2922"]
res_parse_format=[1,0]
input_parse_data=["10.191.170.29/22","10.191.170.2922","10.191.170./22","10.191.-170.29/22","10.191.500.29/22","10.191.A.29/22"]
res_parse_data=[1,0,0,0,0,0]
input_convert_to_bit=["0","192","255"]
res_convert_to_bit=["00000000","11000000","11111111"]
input_convert_to_dec=["0","192","255"]
res_convert_to_dec=["00000000","11000000","11111111"]
for i in range(0,len(input_parse_format)):
    test=parse_format(input_parse_format[i])
    print (test)
    print (res_parse_format[i])
    if (test==res_parse_format[i]):
        print ("Testing func parse_format    OK")
    else:
        print("Testing func parse_format    Error")
for i in range(0,len(input_parse_data)):
    test=parse_data(input_parse_data[i])
    if (test==res_parse_data[i]):
        print("Testing func parse_data    OK")
    else:
        print("Testing func parse_data    Error")
for i in range(0, len(input_convert_to_dec)):
    bin=convert_to_bit(input_convert_to_bit[i])
    dec=convert_to_dec(input_convert_to_dec[i])
    if (bin==res_convert_to_dec[i]):
        print ("Testing func convert_to_dec    OK")
    else:
        print("Testing func convert_to_dec    Error")
    if (dec==res_convert_to_dec[i]):
        print ("Testing func convert_to_dec    OK")
    else:
        print("Testing func convert_to_dec    Error")