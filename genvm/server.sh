#!/bin/bash

if [ "${VSCODEDEBUG}" = "true" ]; then
        python -m debugpy --listen 0.0.0.0:${GENVMDEBUGPORT} genvm/server.py
      else
        python genvm/server.py
      fi