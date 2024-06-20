#!/bin/bash

if [ "${VSCODEDEBUG}" = "true" ]; then
        python -m debugpy --listen 0.0.0.0:${RPCDEBUGPORT} rpc/server.py
      else
        python rpc/server.py
      fi