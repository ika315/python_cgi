#!/usr/bin/python3

import cgi
import cgitb
import os.path
import subprocess

cgitb.enable()
print("Content-type:text/html\n\n")

HTML_START = """
<html>
<head>
<title></title>
</head>
<body>
  <div id="header" style="background-color:#008cff;text-align:center">
    <h1 style="margin-bottom:0;">Compute GC content for any fasta file</h1>
  </div>
  <div id="menu" style="background-color:#6a95d6; height:100%;float:left;padding: 10px;">
    <b>Menu</b></br>
    <a href="gc_with_cgi.py">Compute GC content</a></br>
  </div>
  <div id="content"> 
"""
HTML_FORM="""
	<form name="input" action="gc_with_cgi.py" method="POST" enctype="multipart/form-data">
		<table>
		<tr> 
		<td align="right">Your fasta file: </td> <td> <input type="file" name="filepath"/> </td> </tr>
		</table>
		<input type="submit" name="submit"/>
	</form>
"""
HTML_END="\t</div>\n</body>\n</html>"

inFileData = None

form = cgi.FieldStorage()
filepath=form.getvalue("filepath")

UPLOAD_DIR="tmp"

out = ""
if "filepath" in form:
    form_file = form['filepath']

    if form_file.filename:
        uploaded_file_path = os.path.join(UPLOAD_DIR, os.path.basename(form_file.filename))
        with open(uploaded_file_path, 'wb') as fout:
            while True:
                chunk = form_file.file.read(100000)
                if not chunk:
                    break
                fout.write(chunk)
        out = subprocess.check_output(["python3", "/home/k/kaciran/public_html/scripts/computing_gc.py", "-f", uploaded_file_path])
        if out != None:
            out = out.decode("utf-8", "ignore")

print(HTML_START)
if len(out):
    print(out)
else:
    print(HTML_FORM)
print(HTML_END)