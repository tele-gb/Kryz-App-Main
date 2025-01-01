####Credit card/loan payment calcuations
# import matplotlib.pyplot as plt

glist = []
max_mnths=[]
master=[]

def build(bal , apr , pay_pct, count,add_pay):
    ls =[bal,apr,pay_pct,count,add_pay]
    master.append(ls)

build(3000,0.229,0.025,0,0)
build(5000,0.229,0.025,0,0)
build(10000,0.229,0.025,0,0)

print(master)
[[3000, 0.229, 0.025, 0, 0], [5000, 0.229, 0.025, 0, 0], [10000, 0.229, 0.025, 0, 0]]

#build(3000,0.229,0.025,0,0)

def unpack():
    alist = []
    for i in range(len(master)):        
        a = master[i][0]
        b = master[i][1]
        c = master[i][2]
        d = master[i][3]
        e = master[i][4]
        alist =[a,b,c,d,e]
        print(alist)

        big_lst=[]
        bal_lst=[]
        int_lst=[]
        pay_lst = []
        mnths=[]

        def clist (alist):
            cbal = alist[0]
            count = alist[-2];   
            while cbal > 0:
                count  = count + 1
                int_amt = round(cbal*(alist[1]/12),2)
                pay_amt = round(max(cbal*alist[2],5),2)
                nbal = cbal+int_amt-pay_amt-alist[-1]
                cbal = round(nbal,2)  
                int_lst.append(int_amt)
                bal_lst.append(cbal)
                # mnths.append(count)
            # print(max(mnths)/12)   
            print(count/12)
            print(round(sum(int_lst)))
            glist.append(bal_lst)
            max_mnths.append(count)
            print(bal_lst)
        clist(alist)
        alist.clear()
        
unpack()
print(max(max_mnths))
# xax = list(range(max(max_mnths)))
# print(xax)

# plt.xlabel("Months")
# plt.ylabel("Balance")
# plt.title("CreditCards")
# for i in range(len(glist)):
#     plt.plot(xax,[pt[i] for pt in glist])
# # plt.legend()
# plt.show()
# import matplotlib.pyplot as plt
# import matplotlib.pyplot as pypl

# for card in glist:
#    balcurve = plt.plot(card)
#    balcurve = plt.xlabel('months')
#    balcurve = plt.ylabel('balance')

# plt.show()
