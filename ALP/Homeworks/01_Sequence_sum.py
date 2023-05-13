nums = list(map(int, input().split()))
maxlands = dict()

length = 0
sum = 0

def isPrime(n):
    if n==1 or n==0:
        return False
    else:
        for i in range(2,int(n/2)+1):
            if (n%i) == 0:
                return False
        return True 



for i in range(len(nums)-1):
    if nums[i] > nums[i+1] and isPrime(abs(nums[i]))==False and isPrime(abs(nums[i+1]))==False:
        length += 1
        if length == 1:
            length += 1
            sum = nums[i] + nums[i+1]
        if length > 2:
            sum += nums[i+1]
    else:
        if length not in maxlands:
            maxlands[length] = list()
        maxlands[length].append(sum)
        sum = 0
        length = 0


if length not in maxlands:
    maxlands[length] = list()
maxlands[length].append(sum)

for i in range(len(nums)):
    if isPrime(nums[i]) == True:
        continue
    else:
        if 1 not in maxlands:
            maxlands[1] = list()
        maxlands[1].append(nums[i])

maxlength = max(maxlands.keys())

print(maxlength)
print(max(maxlands[maxlength]))

