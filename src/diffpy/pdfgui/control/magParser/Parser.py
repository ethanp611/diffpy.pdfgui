
class Parser:
	def __init__(self, file_dict):
		self.file_dict = file_dict

	def ReadFile(self, filename):
		file = open(filename, "r")

		while True:
			line = file.readline()

			if not line:
				break

			line = line.split()

			if not line:
				continue

			self.parse(line, file)

		file.close()
		return self.file_dict

	def parse(self, line, file):
		if line[0].find("_") == 0:
			self.insert_dictionary(line)

		elif line[0] == "loop_": 
			keys = []
			values = {} 
			counter = 0

			while True:
				l = file.readline()
				l = l.strip()
				if not l:
					break
				if l.find("_") == 0:
					keys.append(l)
				else:
					l = l.split()
					values[counter] = l 
					counter += 1
			self.insert_loop(keys, values)

	def insert_loop(self, keys, values): 
		for i in values:
			for k in range(len(keys)):
				if keys[k] in self.file_dict:
					self.file_dict[keys[k]].append(values[i][k])
					continue
		
				self.file_dict[keys[k]] = [values[i][k]]

	def insert_dictionary(self, line):
		if line[0] in self.file_dict:
			self.file_dict[line[0]].append(self.to_numeric(self.to_string(line)))
			return 
		
		self.file_dict[line[0]] = [self.to_numeric(self.to_string(line))]

	def to_string(self, line):
		str_1 = ""
		for i in range (1, len(line)):
			str_1 += line[i] + " "
				
		return str_1.strip()

	def to_numeric(self, x):
		if x.isdigit() == True or self.check_float(x) == True:
			return float(x) 
		return x

	def check_float(self, num):
		try:
			float(num)

			return True
		
		except ValueError:
			return False
	