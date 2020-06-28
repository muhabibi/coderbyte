def HistogramArea():

    arr = [6,3,1,4,12,4]
    stack = list()
    largest = 0
    i=0

    while i < len(arr): 
        print('i = ',i,' arr val = ',arr[i])

        if not stack:
            print('stack kosong')
        else:
            print(arr[stack[-1]], ' <= ', arr[i])
        if not stack or arr[stack[-1]] <= arr[i]:
            
            stack.append(i)
            print('append  =', arr[i])
            print(stack)
            i+=1
        else:
            tops = stack.pop()
            print('pop =', arr[tops])
            luas = arr[tops] * ((i - stack[-1] - 1) if stack else i)
            print('luas ',luas)
            largest = max(largest, luas)
            print('largest', largest)


        print()

    while stack:
        tops = stack.pop()
        luas = arr[tops] * ((i - stack[-1] - 1) if stack else i)

    return largest

def main():
    print(HistogramArea())

if __name__ == "__main__":
    main()

# print(HistogramArea(input()))
