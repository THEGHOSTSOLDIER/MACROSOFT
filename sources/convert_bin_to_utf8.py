# convert a binary file to UTF-8 encoded file (for example, a .bin file to a .txt file)
#
# usage : python3 convert_bin_to_utf8.py <input_file> <output_file>
#
# example : python3 convert_bin_to_utf8.py /tmp/secret.bin /tmp/secret.txt

import sys

# check the number of arguments
if len(sys.argv) != 3:
    print("usage : python3 convert_bin_to_utf8.py <input_file> <output_file>")
    sys.exit(1)

# get the input and output file
input_file = sys.argv[1]
output_file = sys.argv[2]

# read the input file
with open(input_file, "rb") as f:
    data = f.read()

# convert the data to UTF-8
data = data.decode("utf-8")

# write the data to the output file
with open(output_file, "w", encoding='utf8') as f:
    f.write(data)

# print a message
print(f"File {input_file} converted to {output_file}")

# end of script