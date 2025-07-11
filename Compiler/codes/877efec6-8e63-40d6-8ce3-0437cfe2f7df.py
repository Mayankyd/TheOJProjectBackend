import sys
input_data = sys.stdin.read().splitlines()
n = int(input_data[0])
nums = list(map(int, input_data[1].split()))
target = int(input_data[2])

for i in range(n):
    for j in range(i + 1, n):
        if nums[i] + nums[j] == target:
            print(f"[{i},{j}]")
            exit()