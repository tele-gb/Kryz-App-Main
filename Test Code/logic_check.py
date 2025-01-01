bal="2000"
apr="29.9"
min_pay="5"
its=0
total_int=0


cbal=int(bal)
while cbal > 0:
    its = its + 1
    int_amt = round(cbal*((float(apr)/100)/12),2)
    pay_amt = round(max(cbal*(int(min_pay)/100),5),2)
    nbal = cbal+int_amt-pay_amt
    cbal = round(nbal,2)  
    total_int = total_int+int_amt
    print(cbal)
    print(its)
print(its/12)

