from tempfile import NamedTemporaryFile
import os
import tempfile

f = NamedTemporaryFile(delete=False)
print f.name
f.write("Hello World!\n")
f.close()
os.unlink(f.name)
print os.path.exists(f.name)
