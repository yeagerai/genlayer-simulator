#!/bin/bash

if [ "${VSCODEDEBUG}" = "true" ]; then
        echo "!!! Starting server in DEBUG mode !!!"
        python -m debugpy --listen 0.0.0.0:${RPCDEBUGPORT} rpc/server.py
      else
        echo "!!! Starting server in HOT RELOAD mode !!!"
        python rpc/server.py
      fi