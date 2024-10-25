#!/usr/bin/env bash
#
docker run -itd --add-host=host.docker.internal:host-gateway --rm -v "${PWD}:/app" footprintai/fed-multimodal-restcol:v0.0.1
