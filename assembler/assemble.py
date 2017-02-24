import struct,argparse
verbose = False

# Helpers

def hex_to_dec(hexstr):
#	print hexstr
	hex = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
	hexstr = hexstr[::-1]
#	print hexstr
	values = []
	curr_place = 0
	for char in hexstr:
		value = hex.index(char)*(16**curr_place)
#		print "{} in place {!s} = {!s}".format(char,curr_place,value)
		values.append(value)
		curr_place += 1
	return sum(values)

def check_gt(value,max,msg,line):
	if value > max:
#		print str(value)+">"+str(max)
		print "Error on line \"{}\": {}".format(line,msg)
		exit(-1)

def check_byte(value,line):
#	print "Checking byte "+str(value)
	check_gt(value,255,"invalid byte",line)

def check_address(address,line):
	check_gt(address,65535,"invalid address",line)

# Functions for assembling DPL code

def assemble_line(line,mercyopcode=""):
	if line.find(";") != -1:
		line = line.split(";",2)[0]
	parts = line.split(" ")
	if parts[0] == "NOP":
		return [0]
	elif parts[0] == "LDA":
		if mercyopcode != "":
			line = mercyopcode+" "+parts[1]
		if parts[1].find("(") == 0:
			check_address(hex_to_dec(parts[1][2:-1]),line)
			return [2,hex_to_dec(parts[1][2:-1])]
		else:
			check_byte(hex_to_dec(parts[1][2:]),line)
			return [1,hex_to_dec(parts[1][2:])]
	elif parts[0] == "ADD":
		check_byte(hex_to_dec(parts[1][2:]),line)
		return [3,hex_to_dec(parts[1][2:])]
	elif parts[0] == "SUB":
		check_byte(hex_to_dec(parts[1][2:]),line)
		return [4,hex_to_dec(parts[1][2:])]
	elif parts[0] == "STA":
		check_address(hex_to_dec(parts[1][2:-1]),line)
		return [5,hex_to_dec(parts[1][2:-1])]
	elif parts[0] == "LDX" or parts[0] == "LDY":
		val = assemble_line("LDA "+parts[1],mercyopcode=parts[0])
		lastletter = parts[0][-1]
		if val[0]==1:
			if lastletter == "X":
				val[0] = 6
			elif lastletter == "Y":
				val[0] = 9
		elif val[0]==2:
			if lastletter == "X":
				val[0] = 7
			elif lastletter == "Y":
				val[0] = 10
		return val
	elif parts[0][:1] == "ST" and parts[0][-1] in ("X","Y"):
		val = assemble_line("STA "+parts[1],mercyopcode=parts[0])
		lastletter = parts[0][-1]
		if lastletter == "X":
			val[0] = 8
		elif lastletter == "Y":
			val[0] = 11
		return val
	elif parts[0][0] == "T":
		from_r = parts[0][1]
		to_r = parts[0][2]
		if from_r == "A":
			if to_r == "X":
				return [13]
			elif to_r == "Y":
				return [15]
		elif from_r == "X":
			if to_r == "A":
				return [12]
		elif from_r == "Y":
			if to_r == "A":
				return [14]
	elif parts[0] == "MBS":
		check_gt(hex_to_dec(parts[1][2:]),2,"invalid memory bank to switch to",line)
		return [16,hex_to_dec(parts[1][2:])]
	elif parts[0] == "JMP":
		check_address(hex_to_dec(parts[1][1:]),line)
		return [17,hex_to_dec(parts[1][1:])]
	elif parts[0] == "CALL":
		check_address(hex_to_dec(parts[1][1:]),line)
		return [18,hex_to_dec(parts[1][1:])]
	elif parts[0] == "RTS":
		return [19]
	return []

def assemble_lines(lines):
	output = []
	for line in lines:
		if line=="":
			continue
		if verbose:
			print "Assembling \"{}\"".format(line.rstrip())
		output.extend(assemble_line(line.rstrip()))
	return output

def assemble_file(file,out="output.bin"):
	with open(file) as f:
		with open(out,"wb") as of:
			values = assemble_lines(f.readlines())
			for value in values:
				if value < 256:
					of.write(struct.pack("B",value))
				else:
					of.write(struct.pack(">H",value))
parser = argparse.ArgumentParser(description="Assemble DPL assembly file <input> into a DPL ROM.")
parser.add_argument("--verbose","-v",action="store_true",dest="verbose",help="Give info on which lines are being assembled.")
parser.add_argument("input",help="The input file.")
parser.add_argument("--output","-o",action="store",dest="outname",help="Name of output ROM. Defaults to \"output.bin\".")
args = parser.parse_args()
verbose = args.verbose
if args.outname:
	assemble_file(args.input,out=args.outname)
else:
	assemble_file(args.input)
