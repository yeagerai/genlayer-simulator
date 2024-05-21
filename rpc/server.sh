#!/bin/bash

if [ "${VSCODEDEBUG}" = "true" ]; then
        echo "!!! VSCode Debugging Enabled !!!"
        echo "(you can attach the debugger to the rpc container)"
        python -m debugpy --listen 0.0.0.0:${RPCDEBUGPORT} rpc/server.py
      else
        echo "!!! Flask Hot Reloading Enabled !!!"
        echo "(changes to files will result in Flask reloading)"
        python rpc/server.py
      fi