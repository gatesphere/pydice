#!/usr/bin/env python
#@+leo-ver=5-thin
#@+node:peckj.20130627092551.2209: * @file dice.py
#@@first
#@@language python

#@+<< imports >>
#@+node:peckj.20130627092551.2210: ** << imports >>
import cgi
import random
import smtplib

## enable traceback on exceptions
import cgitb; cgitb.enable()
#@-<< imports >>
#@+<< declarations >>
#@+node:peckj.20130627092551.2211: ** << declarations >>
## campaigns and lists
campaignlist = {
  'Campaign 1': 'test1@example.com',
  'Campaign 2': 'test2@example.com'
}

## passcode (required to actually use it)
passcode = 'somepasscode'

## email settings
emailinfo = {
  'user': 'user@gmail.com',
  'password': 'password',
  'server': 'smtp.gmail.com',
  'port': 587
}
#@-<< declarations >>

#@+others
#@+node:peckj.20130627092551.2219: ** html
#@+node:peckj.20130627092551.2214: *3* print_header
def print_header():
  print "Content-type: text/html"
  print
#@+node:peckj.20130627092551.2217: *3* print_page
def print_page(results):
  global campaignlist
  print """
<html>
<head>
  <title>Dice!</title>
</head>
<body>
  <center>
    <h1>Dice</h1>
"""
  if results['success']:
    print_results(results)
  else:
    print_error(results)
    print_form()

  print """
  </center>
</body>
</html>
"""
  
#@+node:peckj.20130627092551.2222: *3* print_form
def print_form():
  print """
  <form method='post' action='dice.py'>
    <table>
      <tr>
        <td>Passcode:</td>
        <td><input type='password' name='passcode'></td>
      </tr>
      <tr>
        <td>Campaign:</td>
        <td><select name='campaign'>
"""

  # construct the campaign selection box here
  for c in campaignlist:
    print "<option value='%s'>%s</option>" % (c,c)

  print """
            </select></td>
      </tr>
      <tr>
        <td>Roll type:</td>
        <td><input type='text' name='rolltype'></td>
      <tr>
      <tr>
        <td>Your name:</td>
        <td><input type='text' name='playername'></td>
      <tr>
        <td>Comment: </td>
        <td><input type='text' name='comment'></td>
      </tr>
      <tr>
        <td></td>
        <td><input type='submit' value='Roll!'></td>
      </tr>
    </table>
    </form>
"""
#@+node:peckj.20130627092551.3121: *3* print_results
def print_results(results):
  print results
#@+node:peckj.20130627092551.3122: *3* print_error
def print_error(results):
  print results
#@+node:peckj.20130627092551.2223: ** dice
#@+node:peckj.20130627092551.2224: *3* parse_dicestring
def parse_dicestring(diestring):
  values = []
  fudgedice = [-1, 0, 1]
  essence = False
  diestring2 = diestring.replace("-", " -")
  diestring2 = diestring2.replace("+", " ")
  dice = diestring2.lower().split()
  for die in dice:
    if die.find('d') != -1:
      num = die[0:die.index('d')]
      num = (1 if num == '' else int(num))
      s = die[die.index('d')+1:]
      if 'f' in s:
        for i in range(num):
          values.append(random.choice(fudgedice))
      else:
        sides = int(s)
        for i in range(num):
          values.append(random.randrange(1, sides+1))
      if 'e' in s:
        essence = random.choice(fudgedice)
    else:
      values.append(int(die))
  return (values, essence)
#@+node:peckj.20130627092551.2220: ** cgi
#@+node:peckj.20130627092551.2215: *3* grab_request_info
def grab_request_info():
  req_info = {}
  form = cgi.FieldStorage()
  
  req_info['passcode']   = form.getvalue('passcode')
  req_info['campaign']   = form.getvalue('campaign')
  req_info['rolltype']   = form.getvalue('rolltype')
  req_info['playername'] = form.getvalue('playername')
  req_info['comment']    = form.getvalue('comment')
  
  return req_info
#@+node:peckj.20130627092551.2216: *3* run_request
def run_request(req_info):
  results = {'success': True}
  
  ## validate info - if any field is blank, error out
  for f in req_info:
    if req_info[f] is None:
      results['success'] = False
      results['message'] = "Invalid form.  Please try again."
      break
  
  if results['success']:
    ## roll dice
    dice = parse_dicestring(req_info['rolltype'])
    message = "Results for roll %s: %s (total %s)" % (req_info['rolltype'], dice[0], sum(dice[0]))
    if dice[1]:
      message += " Essence die: %s" % dice[1]
    results['success'] = True
    results['message'] = message
    ## send email
  
  ## return results to pass to print_page (handled by main)
  return results
  pass
#@+node:peckj.20130627092551.2221: ** email
#@+node:peckj.20130627092551.2218: *3* send_email
def send_email(to, subject, message):
  global emailinfo
  
  header = 'To: ' + to + '\n'
  header += 'From: ' + emailinfo['user'] + '\n'
  header += 'Subject: ' + subject + '\n\n'
  
  message = header + message
  
  server = smtplib.SMTP(emailinfo['server'], emailinfo['port'])
  server.ehlo()
  server.starttls()
  server.login(emailinfo['user'], emailinfo['password'])
  server.sendmail(emailinfo['user'], to, message)
  server.close()

#@+node:peckj.20130627092551.2212: ** main
def main():
  req_info = grab_request_info()
  results = run_request(req_info)
  print_header()
  print_page(results)
#@-others

main()
#@-leo
