[![Python 2.7 3.7](https://img.shields.io/badge/python-2.7%20%7C%203.7-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Documentation
This repository is a part of the ShotGrid Pipeline Toolkit.

- For more information about this app and for release notes, *see the wiki section*.
- For general information and documentation, click here: https://developer.shotgridsoftware.com/d587be80/?title=Integrations+User+Guide
- For information about ShotGrid in general, click here: http://www.shotgridsoftware.com/toolkit

## Using this app in your Setup
All the apps that are part of our standard app suite are pushed to our App Store.
This is where you typically go if you want to install an app into a project you are
working on. For an overview of all the Apps and Engines in the Toolkit App Store,
click here: https://developer.shotgridsoftware.com/162eaa4b/?title=Pipeline+Integration+Components

## Have a Question?
Don't hesitate to contact us! Please visit our web site https://developer.shotgridsoftware.com for help.

## Flame Engine Logging
The Flame engine logs information to `/opt/Autodesk/log/tk-flame.log`. This is helpful if you are trying
to troubleshoot or debug.

## Flame Engine Bootstrap
The Flame engine uses a more complex bootstrap than most other engines
and it runs in three different states - before Flame launches, during Flame operation,
and as part of backburner jobs.

For details around the bootstrap, see comments in individual files. Below is a summary of how
Flame is typically being launched:

- The multi launch app (or equivalent) reaches into `python/startup/bootstrap.py` and passes DCC launch paths
  and arguments. This method tweaks library paths and a few other minor things and returns a
  set of *rewritten* paths, where the main launch binary now is a script inside the flame engine.
  For example, the multi launch app may pass the following parameters into the bootstrap script:

  ```
  app_path: /opt/Autodesk/flame_<version>/bin/startApplication
  app_args: --extra args
  ```

  The bootstrap script then returns the following:

  ```
  app_path: /opt/Autodesk/python/<flame version>/bin/python
  app_args: /mnt/software/shotgun/my_project/install/engines/app-store/tk-flame/v1.2.3/startup/launch_app.py
            /opt/Autodesk/flame_<version>/bin/startApplication
            --extra args
  ```

- The multi launch app now executes the re-written DCC path and thereby starts executing `python/startup/launch_app.py`.
  inside the python interpreter which comes bundled with Flame (and contains a known version of PySide). The engine starts
  up, hooks paths are registered by setting the `DL_PYTHON_HOOK_PATH` environment variable etc.
  At this point, a check is carried out to see if a Flame project corresponding to the ShotGrid project exists or not.
  If it doesn't, a project setup UI is shown on screen where a user can configure a new Flame project.

- Once a Project has been established, the Flame DCC is launched.
