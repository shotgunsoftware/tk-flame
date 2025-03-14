[![VFX Platform](https://img.shields.io/badge/vfxplatform-2025%20%7C%202024%20%7C%202023%20%7C%202022-blue.svg)](http://www.vfxplatform.com/)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.10%20%7C%203.9-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Documentation
This repository is a part of the Flow Production Tracking Toolkit.

- For more information about this app and for release notes, *see the wiki section*.
- For general information and documentation, click here: https://help.autodesk.com/view/SGDEV/ENU/?contextId=SA_INTEGRATIONS_USER_GUIDE
- For information about Flow Production Tracking in general, click here: https://www.autodesk.com/products/shotgrid/overview

## Using this app in your Setup
All the apps that are part of our standard app suite are pushed to our App Store.
This is where you typically go if you want to install an app into a project you are
working on. For an overview of all the Apps and Engines in the Toolkit App Store,
click here: https://help.autodesk.com/view/SGDEV/ENU/?contextId=PC_TOOLKIT_APPS

## Have a Question?
Don't hesitate to contact us at https://www.autodesk.com/support/contact-support for help.

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
  At this point, a check is carried out to see if a Flame project corresponding to the Flow Production Tracking project exists or not.
  If it doesn't, a project setup UI is shown on screen where a user can configure a new Flame project.

- Once a Project has been established, the Flame DCC is launched.
