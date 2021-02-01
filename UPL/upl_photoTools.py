from PIL import Image
from UPL.Core import file_exists

"""
Converts any image file to an icon file
"""
def img2ico(infile, outfile, sizes=[(48,48)]):
	if outfile.endswith(".ico"):
		if file_exists(infile):
			img = Image.open(infile)
			img.save(outfile, sizes=sizes)

		else:
			return f"{infile} does not exists or cannot be opened"
	else:
		return f"{outfile} cannot be grabbed"
