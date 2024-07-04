program = """print("Hello, World!")"""

filename = "text.txt"

with open(filename, "w") as file:
    file.write(program)
