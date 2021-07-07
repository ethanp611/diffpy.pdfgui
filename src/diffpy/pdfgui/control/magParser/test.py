import Parser

file_dict = {}

object = Parser.Parser(file_dict)

file_dict = object.ReadFile("0.6_YMnO3.mcif")

print("Example: ")
print("propagation vector: ")
print(file_dict["_parent_propagation_vector.kxkykz"])