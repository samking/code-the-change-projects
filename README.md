Code the Change Projects
========================

A projects database for projects at the intersection of CS and social change.

# Setup

* Clone this repo.  You may want to rename the folder to ctc-projects for
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
* Go to [http://localhost:8080/]() to see the site running or
  [http://localhost:8000/]() to see the admin console.
* You don't need to do anything to deploy code to production.  Pushing to git
  will deploy.

# Style

* Please adhere to the relevant Google Style Guides:
  [Python](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html),
  [Javascript](https://google-styleguide.googlecode.com/svn/trunk/javascriptguide.xml),
  [HTML/CSS](https://google-styleguide.googlecode.com/svn/trunk/htmlcssguide.xml)).
