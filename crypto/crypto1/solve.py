#!/usr/bin/env python3

# The parameters (scramble wheels and bramble keys) are identical to the original code
scramble_wheels = [
    [54, 9, 24, 45, 1, 15, 13, 4, 47, 31, 16, 57, 36, 58, 32, 46, 7, 40, 6, 39, 14, 11, 50, 44, 52, 21, 19, 30, 8, 55, 34, 43, 3, 49, 0, 28, 53, 22, 17, 23, 18, 56, 51, 27, 48, 20, 29, 37, 2, 10, 35, 38, 25, 41, 33, 5, 12, 42, 26],
    [51, 19, 10, 43, 26, 38, 48, 13, 41, 2, 53, 9, 3, 28, 45, 35, 54, 29, 7, 0, 25, 17, 47, 56, 55, 5, 6, 32, 39, 40, 21, 30, 22, 12, 16, 27, 20, 34, 36, 31, 58, 24, 33, 15, 11, 1, 50, 44, 14, 49, 8, 46, 4, 57, 18, 42, 37, 23, 52],
    [16, 14, 11, 7, 54, 4, 41, 46, 36, 55, 13, 37, 53, 18, 5, 9, 29, 2, 24, 27, 15, 43, 6, 22, 49, 31, 33, 48, 10, 40, 39, 44, 52, 25, 38, 57, 8, 47, 34, 30, 17, 23, 42, 51, 58, 50, 12, 3, 0, 32, 28, 21, 45, 1, 35, 26, 56, 20, 19]
]

bramble_keys = [
    [252, 124, 88, 199, 15, 171, 250, 101, 132, 103, 151, 251, 237, 14, 91, 118, 8, 7, 73, 14, 222, 212, 172, 46, 99, 103, 112, 207, 133, 210, 145, 226, 29, 182, 184, 125, 162, 50, 80, 116, 89, 73, 184, 78, 211, 93, 12, 89, 27, 235, 84, 64, 164, 180, 254, 211, 37, 254, 108],
    [215, 34, 200, 55, 37, 151, 172, 0, 30, 120, 219, 127, 27, 36, 111, 99, 208, 222, 142, 27, 202, 178, 187, 143, 102, 204, 70, 4, 106, 108, 126, 94, 13, 226, 193, 134, 248, 72, 99, 95, 145, 9, 197, 75, 178, 95, 205, 62, 65, 48, 75, 250, 12, 25, 108, 38, 18, 162, 91],
    [135, 107, 236, 31, 136, 226, 135, 81, 136, 102, 108, 97, 209, 56, 161, 20, 143, 49, 32, 7, 75, 169, 8, 231, 196, 112, 156, 172, 136, 3, 65, 171, 33, 95, 62, 194, 84, 162, 161, 15, 229, 117, 23, 87, 123, 21, 94, 159, 99, 181, 249, 111, 164, 180, 2, 3, 32, 144, 127]
]

# This is the final output produced by the original program.
# Replace the below list with the actual output (list of numbers) you obtained.
final_output = eval(open("./output.txt").read().strip())

# Convert the final output into a bytearray for processing.
res = bytearray(final_output)

# Reverse the three rounds (note: round order is reversed)
for i in range(2, -1, -1):
    tmp = bytearray(len(res))
    for j in range(len(res)):
        # For each original position j, undo:
        # original[j] = current[scramble_wheels[i][j]] XOR bramble_keys[i][j]
        tmp[j] = res[scramble_wheels[i][j]] ^ bramble_keys[i][j]
    res = tmp

# Now res holds the original flag
flag = res.decode()
print("Recovered flag:", flag)
