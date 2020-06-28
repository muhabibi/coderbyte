def StockPicker(arr):

  largest=0
  delta=0

  for i in range(len(arr)):
    for j in range(i+1, len(arr)):
      if arr[j] > arr[i]:
        delta = arr[j]-arr[i]
        largest = max(delta, largest)
      else:
        continue
  
  if largest==0 :
    largest = -1

  return largest
 
def main():
  arr=[10, 9, 8, 2]
  print(StockPicker(arr))

if __name__ == "__main__":
    main()
