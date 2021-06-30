import random
import time

how = 5000
howtest = 20000
forme = 0
count = 0

for i in range(how):
    ifme = 0
    
    for i in range(howtest):
        a = random.randint(1, 100)
        
        if a == 1:
            ifme += 1
    
    count += 1
        
    print(str(round(ifme / howtest * 100, 2)) + " % : TSC - " + str(ifme) + " : 정산 확률 - " + str(round(forme / count, 2)) + " %")
    forme += round(ifme / howtest * 100, 10)

print("최종 확률은 " + str(round(forme / how, 5)) + "% 입니다")