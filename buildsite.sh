#!/bin/bash

skaffold build -q >build.out && skaffold deploy -a build.out && rm build.out
