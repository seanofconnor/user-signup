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
import cgi
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

template = """
<!DOCTYPE html>

<html>
    <head>
    </head>
    <body>
    <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="{username}" required>
                        <span class="error">{error_username}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error">{error_password}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error">{error_verify}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="{email}">
                        <span class="error">{error_email}</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
    </body>
</html>
"""

def renderPage(username='', error_username='', error_password='', error_verify='', email='', error_email=''):
    page = template.format(username = username, error_username = error_username, error_password = error_password, error_verify = error_verify, email = email, error_email = error_email)
    return page


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/signup')

class Signup(webapp2.RequestHandler):
    def get(self):
        self.response.write(renderPage())

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        have_error = False

        if not valid_username(username):
            error_username = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            error_password = " That wasn't a valid password."
            have_error = True

        elif password != verify:
            error_verify = " Your passwords don't match."
            have_error = True

        if not valid_email(email):
            error_email = " That's not a valid email."
            have_error = True

        if have_error:
            self.response.write(renderPage(page))
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
