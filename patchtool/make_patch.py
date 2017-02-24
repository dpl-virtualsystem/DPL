import argparse,struct,os.path
parser = argparse.ArgumentParser(description="Creates and applies patches to binaries.")
parser.add_argument("--apply","-a",action="store_true",help="The program treats file1 as a fresh file and file2 as a patch. Applies file2 to file1.")
parser.add_argument("file1",help="The first binary. Used as clean binary for applying patches.")
parser.add_argument("file2",help="The second binary. Considered the modified binary. When applying patches, this is the patch to apply.")
args = parser.parse_args()
file1 = []
file2 = []
if not args.apply:
	with open(args.file1) as f:
		raw_contents = f.read()
		file1 = struct.unpack("B"*len(raw_contents),raw_contents)
	with open(args.file2) as f:
		raw_contents = f.read()
		file2 = struct.unpack("B"*len(raw_contents),raw_contents)
	patch = ""
	org = 0
	currently_modifying = False
	file1_tapped = False
	while org < len(file2):
		vf1 = 0
		vf2 = file2[org]
		if org < len(file1):
			vf1 = file1[org]
		else:
			file1_tapped = True
		if file1_tapped or file1[org] != file2[org]:
			if not currently_modifying:
				patch += "@org {!s}\n{!s},".format(org,file2[org])
				currently_modifying = True
			else:
				patch += str(file2[org])+","
		else:
			if currently_modifying:
				currently_modifying = False
				patch = patch[:-1]+"\n"
		org = org + 1
	print(patch[:-1])
else:
	with open(args.file1) as f:
		raw_contents = f.read()
		file1 = list(struct.unpack("B"*len(raw_contents),raw_contents))
	patch = []
	with open(args.file2) as f:
		patch = [s.rstrip() for s in f.readlines()]
		patch = filter(None,patch)
	org = 0
	for line in patch:
		if line.find("@org ") == 0: # is this an org directive?
			org = int(line.split(" ")[1]) #if so, set our position in the file according
		else:
			for num in [int(s) for s in line.split(",")]:
				file1[org] = num
				org += 1
	name, ext = os.path.splitext(args.file1)
	with open(name+"_patched"+ext,"wb") as f:
		f.write(struct.pack("B"*len(file1),*file1))
