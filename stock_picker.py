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
  return largest

# keep this function call here 
print(StockPicker(input()))
