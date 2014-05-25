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
* Run `dev_appserver.py .` to run a local server.  Note that this is in the
  Cloud SDK, not this project's directory.
* Go to [http://localhost:8080/](http://localhost:8080/) to see the site running
  or [http://localhost:8000/](http://localhost:8000/) to see the admin console.
* When you're ready to submit your code, submit a pull request with the base in
  this repo and the changes in your repo.  Then, there will be a code review,
  and when that's done, we'll merge the branches.
* You don't need to do anything to deploy code to production.  When the pull
  request is accepted, it will be deployed automatically.

# Testing

* Install `easy_install`: `sudo apt-get install python-setuptools` in
  Ubuntu.  pip or other Python package installers should work as well.
* Install `nose` (a test runner for Python): `sudo easy_install nose` in
  Ubuntu.
* Install `NoseGAE` (a nose plugin for Google App Engine that sets up the
  app engine environment and runs tests):
  `sudo easy_install NoseGAE` in Ubuntu.
* Install `webtest` (an integration testing framework for webapps):
  `sudo easy_install webtest` in Ubuntu.
* Install `mock` (a mock framework that is standard in Python 3):
  `sudo easy_install mock` in Ubuntu.
* Install `coverage` (a tool that lets you see what code you're actually
  testing): `sudo easy_install coverage` in Ubuntu.
* Now, whenever you want to run tests, all you have to do is run
  `scripts/test.py` (which will run nosetests for you, looking up your app
  engine directory from your PATH).  You can also run the tests manually, but
  that would require properly setting the PYTHONPATH (eg, using
  `scripts.common.fix_app_engine_path()`).  Please make sure that you fix all
  tests before submitting code (as well as testing new features you add).
* After testing, you should run `scripts/coverage.py` to make sure that your
  tests actually exercise all of your code.

# Style

* Install pylint.  Use `sudo apt-get install pylint` in Ubuntu.
* Please adhere to the relevant Google Style Guides:
  [Python](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html),
  [Javascript](https://google-styleguide.googlecode.com/svn/trunk/javascriptguide.xml),
  [HTML/CSS](https://google-styleguide.googlecode.com/svn/trunk/htmlcssguide.xml)).
* Please run `scripts/lint.py` and fix all warnings or silence them in the
  .pylintrc or locally in the file (depending on the issue) before submitting
  code.
