#!/usr/bin/python  

import cgitb
import cgi

cgitb.enable() #This will show any errors on your webpage

inputs = cgi.FieldStorage() #REMEMBER: We do not have inputs, simply a button to run the program. In order to get inputs, give each one a name and call it by inputs['insert_name']

print "Content-type: text/html" #We are using HTML, so we need to tell the server

print #Just do it because it is in the tutorial :P

print "<title> MyPythonWebpage </title>"

print "Whatever you would like to print goes here, preferably in between tags to
