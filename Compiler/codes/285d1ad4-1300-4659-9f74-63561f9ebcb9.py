import sys
input_data = sys.stdin.read().splitlines()
n = int(input_data[0])
nums = list(map(int, input_data[1:n+1]))
target = int(input_data[n+1])

for i in range(n):
    for j in range(i + 1, n):
        if nums[i] + nums[j] == target:
            print(f"[{i},{j}]")
            exit()