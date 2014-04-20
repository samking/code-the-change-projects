Code the Change Projects
========================

A projects database for projects at the intersection of CS and social change.

# Setup

* Fork this repo.  This will make pull requests and code review easier.
* Clone the forked repo.  You may want to rename the folder to ctc-projects for
  convenience.
* Install Google Cloud SDK: https://developers.google.com/cloud/sdk/
* Make sure that you add the path and completion modules to your shell's startup
  file.  Assuming you use bash, the Cloud SDK installer should do this for you.
  You will need to restart your shell, re-import your config file (`source
  ~/.bashrc`), or re-run your shell (`bash`).

# Development

* Go to the project directory (`cd ~/code-the-change-projects` if you cloned the
  repo in your home directory).
* Run `dev_appserver.py .` to run a local server.
* Go to [http://localhost:8080/](http://localhost:8080/) to see the site running or
  [http://localhost:8000/](http://localhost:8000/) to see the admin console.
* When you're ready to submit your code, submit a pull request with the base in
  this repo and the changes in your repo.  Then, there will be a code review,
  and when that's done, we'll merge the branches.
* You don't need to do anything to deploy code to production.  When the pull
  request is accepted, it will be deployed automatically.

# Style

* Please adhere to the relevant Google Style Guides:
  [Python](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html),
  [Javascript](https://google-styleguide.googlecode.com/svn/trunk/javascriptguide.xml),
  [HTML/CSS](https://google-styleguide.googlecode.com/svn/trunk/htmlcssguide.xml)).
* Please run `scripts/lint.py` and fix all warnings or silence them in the
  .pylintrc or locally in the file (depending on the issue) before submitting
  code.
