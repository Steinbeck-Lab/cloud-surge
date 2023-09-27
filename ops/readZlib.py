import zlib

with open("output_file", "rb") as myfile:
    S = myfile.read()
    T = zlib.decompress(S)
    print(T)
