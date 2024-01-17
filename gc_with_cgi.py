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
    <div id="head" style="background-color: pink; text-align: center;">
      <h1 style="margin-bottom: 0; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Compute GC content for a fasta file</h1> 
    </div>
    <div id="menu" style="background-color: mistyrose; text-align: center; height:100%;float:left;padding: 10px;">
      <h4 style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;"><b>Menu</b></h4></br>
      <a href="gc_with_cgi.py" style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">Compute GC content</a></br>
    </div>
    
    <div id="content" style="text-align: center; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">
    <p>Here you can compute the highest GC content of a sequence in your fasta file. </br>
        A fasta file consists typically of an identifier line starting with a ">" followed by its sequence data, representing the genetic code using nucleotides A, C, T and G.
        Computing the GC content of a sequence helps determine important attributes of DNA or RNA, such as stability. </br>
    </p>
"""
HTML_FORM="""
	  <form name="input" action="gc_with_cgi.py" method="post" enctype="multipart/form-data">
        <table>
          <tr>
            <td>Upload your fasta file here:</td> 
            <td> <input type= "file" name="filepath"/> </td>
          </tr>
          <tr>
            <td>Click to submit your input:</td>
            <td> <input type="submit" name="submit"/>
          </tr>
        </table>
      </form>
"""
HTML_END="\t</div>\n</body>\n</html>"

inFileData = None

# retrieves the form from the html and gets value from filepath
form = cgi.FieldStorage()
filepath=form.getvalue("filepath")

# directory where file uploads get saved
UPLOAD_DIR="tmp"

# checks whether there is a filepath in the form, i.e. if it was an empty upload and saves it to the directory
out = ""
if "filepath" in form:
    form_file = form['filepath']

    if form_file.filename:
        uploaded_file_path = os.path.join(UPLOAD_DIR, os.path.basename(form_file.filename))
        with open(uploaded_file_path, 'wb') as fout:
            while True:
                chunk = form_file.file.read(100000) # reads a chunk of file in size 100000 bytes
                # if empty chunk or end of file reached, break
                if not chunk:
                    break
                fout.write(chunk)
        # after successfully uploading, subprocess module uses external py script
        out = subprocess.check_output(["python3", "/home/k/kaciran/public_html/scripts/computing_gc.py", "-f", uploaded_file_path])
        # if there was an output computed, we translate it from bytes to utf8
        if out != None:
            out = out.decode("utf-8", "ignore")

print(HTML_START)
if len(out):
    max_seq_id, max_content = out.split("\n", 1)
    print(f"<p><b>This is the sequence with the highest GC content: {max_seq_id}</b></p>")
    print(f"<p><b>This is its GC content: {max_content}</b></p>")
else:
    print(HTML_FORM)
print(HTML_END)