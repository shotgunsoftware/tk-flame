# Copyright (c) 2014 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import sys
import pickle

pickle_file = sys.argv[1]

if not os.path.exists(pickle_file):
    raise TankError("Cannot find backburner command file '%s'!" % pickle_file)

fh = open(pickle_file, "rb")
data = pickle.load(fh)
fh.close()

# get the data out of our pickle
sgtk_core_location = data["sgtk_core_location"]
serialized_context = data["serialized_context"]
engine_instance = data["engine_instance"]
app_instance = data["app_instance"]
method_to_execute = data["method_to_execute"]
method_args = data["args"]

# add sgtk to our python path
sys.path.append(sgtk_core_location)
import sgtk

# first, attempt to launch the engine
context = sgtk.context.deserialize(serialized_context)
engine = sgtk.platform.start_engine(engine_instance, context.sgtk, context)
engine.log_debug("Engine launched for backburner process.")

# execute method
app = engine.apps[app_instance]
method = getattr(app, method_to_execute)
engine.log_debug("Executing remote callback for app instance %s (%s)" % (app_instance, app))
engine.log_debug("Executing callback %s with args %s" % (method, method_args))

method(**method_args)

# all done
engine.log_debug("Backburner execution complete.")

# clean up
try:
    engine.log_debug("Trying to remove temporary pickle job file...")
    os.remove(pickle_file)
    engine.log_debug("Temporary pickle job successfully deleted.")
except Exception, e:
    engine.log_warning("Could not remove temporary file '%s': %s" % (pickle_file, e))
    
