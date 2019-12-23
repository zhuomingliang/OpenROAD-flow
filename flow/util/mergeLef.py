#!/usr/bin/env python3
import re
import sys
import os
import argparse  # argument parsing

# WARNING: this script expects the tech lef first

# Parse and validate arguments
# ==============================================================================
parser = argparse.ArgumentParser(
    description='Merges lefs together')
parser.add_argument('--inputLef', '-i', required=True,
                    help='Input Lef', nargs='+')
parser.add_argument('--outputLef', '-o', required=True,
                    help='Output Lef')
args = parser.parse_args()


print(os.path.basename(__file__),": Merging LEFs")

f = open(args.inputLef[0])
content = f.read()
f.close()

# Remove Last line ending the library
content = re.sub("END LIBRARY","",content)

# Iterate through additional lefs
for lefFile in args.inputLef[1:]:
  f = open(lefFile)
  snippet = f.read()
  f.close()

  # Match the sites
  pattern = r"^SITE.*?^END\s\S+"
  m = re.findall(pattern, snippet, re.M | re.DOTALL)

  print(os.path.basename(lefFile) + ": SITEs matched found: " + str(len(m)))
  content += "\n".join(m)

  # Match the macros
  pattern = r"^MACRO.*?^END\s\S+"
  m = re.findall(pattern, snippet, re.M | re.DOTALL)

  print(os.path.basename(lefFile) + ": MACROs matched found: " + str(len(m)))
  content += "\n" + "\n".join(m)


content += "\nEND LIBRARY"

f = open(args.outputLef, "w")
f.write(content)
f.close()

print(os.path.basename(__file__),": Merging LEFs complete")