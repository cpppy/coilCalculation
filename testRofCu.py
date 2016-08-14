import calcHeat



temp = 4.5
for i in range(300):
    temp = temp + 1
    r = calcHeat.RofCu(temp)
    print temp,r
