#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

signup = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
</head>
<body>
    <h1>Signup</h1>
<form method='post'>
    <label>
    Username
    <input type="text" name="username"/>
    </label>
<br>
    <label>
    Password
    <input type="password" name="password"/>
    </label>
<br>
    <label>
    Verify Password
    <input type="password" name="verify"/>
    </label>
<br>
    <label>
    Email (optional)
    <input type="text" name="email"/>
    </label>
<br>
    <input type='submit'>
</form>
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/signup')

class Signup(webapp2.RequestHandler):
    def get(self):
        self.response.write(signup)

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        have_error = False
        error = ""

        if not valid_username(username):
            error_username = "That's not a valid username."
            error = error + error_username
            have_error = True

        if not valid_password(password):
            error_password = " That wasn't a valid password."
            error = error + error_password
            have_error = True

        elif password != verify:
            error_verify = " Your passwords don't match."
            error = error + error_verify
            have_error = True

        if not valid_email(email):
            error_email = " That's not a valid email."
            error = error + error_email
            have_error = True

        if have_error:
            self.response.write(signup + error)
        else:
            self.redirect('/welcome')


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write("Welcome" + username)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', Signup),
    ('/welcome', Welcome)
], debug=True)
