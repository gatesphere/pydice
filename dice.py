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
import time

## enable traceback on exceptions
import cgitb; cgitb.enable()
#@-<< imports >>
#@+<< declarations >>
#@+node:peckj.20130627092551.2211: ** << declarations >>
## campaigns and lists
campaignlist = {
  'games': 'games@suspended-chord.info',
  'gatesphere': 'gatesphere@gmail.com'
}

## passcode (required to actually use it)
passcode = 'mintyfresh'

## email settings
emailinfo = {
  'user': 'dice@suspended-chord.info',
  'password': 'rollthembones',
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
  <script language="javascript">
    alert('ooga');
    function populate(text)
    {
      alert(text);
    }
  </script>
</head>
<body>
  <script>
  alert('boo!');
  </script>
  <center>
    <h1>Dice</h1>
"""
  print_message(results)
  if not results['success']:
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
        <td><input type='text' name='rolltype' id='rolltype'></td>
      </tr>
      <tr>
        <td></td>
        <td><a href="#" id="4dFE" onclick="populate('4dFE')">4dF + Essence</a> | 
            <a href="#" id="4dF" onclick="populate('4dF')">4dF</a> | 
            <a href="#" id="d4" onclick="populate('d4')">d4</a> | 
            <a href="#" id="d6" onclick="populate('d6')">d6</a> |
            <a href="#" id="2d6" onclick="populate('2d6')">2d6</a> |  
            <a href="#" id="3d6" onclick="populate('3d6')">3d6</a> | 
            <a href="#" id="d8" onclick="populate('d8')">d8</a> | 
            <a href="#" id="d10" onclick="populate('d10')">d10</a> | 
            <a href="#" id="d12" onclick="populate('d12')">d12</a> | 
            <a href="#" id="d20" onclick="populate('d20')">d20</a> | 
            <a href="#" id="d100" onclick="populate('d100')">d100</a></td>
      </tr>
      <tr>
        <td>Your name:</td>
        <td><input type='text' name='playername'></td>
      </tr>
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
#@+node:peckj.20130627092551.3121: *3* print_message
def print_message(results):
  print results['message']
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
      try:
        num = int(num)
      except:
        num = 1
      s = die[die.index('d')+1:]
      if 'e' in s:
        essence = random.choice(fudgedice)
      if 'f' in s:
        for i in range(num):
          values.append(random.choice(fudgedice))
      else:
        try:
          sides = int(s)
        except:
          sides = 6
        for i in range(num):
          values.append(random.randrange(1, sides+1))
    else:
      try:
        die = int(die)
      except:
        die = 0
      values.append(die)
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
  global passcode
  results = {'success': True}
  
  ## validate info - if any field is blank, error out
  for f in req_info:
    if req_info[f] is None:
      results['success'] = False
      results['message'] = "Please fill in <b>all</b> fields."
      return results
  
  if results['success'] and req_info['passcode'] == passcode:
    ## roll dice
    dice = parse_dicestring(req_info['rolltype'])
    message = "Roll requested by: %s\n" % req_info['playername']
    message += "For campaign: %s\n" % req_info['campaign']
    message += "Roll comment: %s\n" % req_info['comment']
    message += "Roll timestamp: %s\n" % time.strftime("%Y-%m-%d %H:%M:%S (EST)")
    message += "Results for roll %s:\n%s\n(total %s)" % (req_info['rolltype'], dice[0], sum(dice[0]))
    if dice[1]:
      message += "\nEssence die: %s" % dice[1]
    results['success'] = True
    results['message'] = "<pre>" + message + "</pre>"
    ## send email
    c = req_info['campaign']
    subject = "[***DICE SERVER***] %s: Roll from %s (%s)" % (c, req_info['playername'], req_info['comment'])
    email = campaignlist[c]
    message = "Hello list.  Incoming die roll...\n\n\n" + message
    message += "\n\nDice Server signing off."
    send_email(email, subject, message)
    
  else: # incorrect passcode
    results['success'] = False
    results['message'] = "Invalid passcode.  Please try again."
  
  ## return results to pass to print_page (handled by main)
  return results
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
