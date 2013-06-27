#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:peckj.20130627092551.2209: * @file dice.py
#@@first
#@@language python

#@+<< imports >>
#@+node:peckj.20130627092551.2210: ** << imports >>
import cgi
import cgitb
#@-<< imports >>
#@+<< declarations >>
#@+node:peckj.20130627092551.2211: ** << declarations >>
cgitb.enable()
#@-<< declarations >>

#@+others
#@+node:peckj.20130627092551.2214: ** print_header
def print_header():
  print "Content-type: text/html"
  print
#@+node:peckj.20130627092551.2215: ** grab_request_info
def grab_request_info():
  pass
#@+node:peckj.20130627092551.2216: ** run_request
def run_request(req_info):
  pass
#@+node:peckj.20130627092551.2217: ** print_page
def print_page(results):
  pass
#@+node:peckj.20130627092551.2212: ** main
def main():
  req_info = grab_request_info()
  results = run_request(req_info)
  print_header()
  print_page(results)
#@+node:peckj.20130627092551.2213: ** actually do it all...

main()
#@-others
#@-leo
