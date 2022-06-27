tri_imax = [2,1,3]
num, i = [-1]+2*[0], 0
while i<3:
    if num[i]<tri_imax[i]:
        num[i] += 1
        print(num)
        i = 0
    while i<3 and num[i]==tri_imax[i]:
        num[i] = 0
        i += 1