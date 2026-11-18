
"""mkdir[Make Directory] -> to create a new folder/directory"""
"""rmdir[Remove Directory]-> remove any folder/directory"""

# File

"""
x -> This mode will only create the file, and if it already exists, we will get an error.
w -> If the file does not exist, it will be created, and we can write into it.
a -> Add text at the end of the file.
r -> Read the content saw the inside of the file.
"""

"""Mode 1: x -> just to create the file"""
# open("Garba.txt", "x")

"""Mode 2: w -> if there is any content inside the file, it will replace the old content."""

# file = open("Garba.txt", "w")
# file.write("Khalo bhut khalo din raat khalo")
# file.write("\nKhalo bhut khalo din raat khalo ghar mat aana bapis")


"""Mode 3: a -> add text at the end of the file."""

# file = open("Garba.txt", "a")
# file.write("\nThis message is newly added")

"""Mode 4: r -> read the content inside the file and define the text in the terminal."""

# file = open("Garba.txt", "r")
# print(file.read())
# file.close()

"""With"""

# with open("simple.txt", "w") as file:
#     file.write("This is a new file by Checking purpose")

"""CRUD - CREATE, READ, UPDATE, DELETE"""

# import os
# os.remove("Garba.txt")
