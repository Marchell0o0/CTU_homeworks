def isPrime(n):
    if n <= 1:
        return False
    else:
        for i in range(2, n // 2 + 1):
            if n % i == 0:
                return False
        return True


def main():
    nums = list(map(int, input().split()))
    length = 0
    sum = 0
    max_length = 0
    max_sum = 0
    for i in range(len(nums) - 1):
        if isPrime(nums[i]):
            continue
        sum += nums[i]
        length += 1
        if length > max_length:
            max_length = length
            max_sum = sum
        elif length == max_length and max_sum < sum:
            max_sum = sum

        if nums[i+1] > nums[i]:
            sum = 0
            length = 0

    print(max_length)
    print(max_sum)


if __name__ == "__main__":
    main()
