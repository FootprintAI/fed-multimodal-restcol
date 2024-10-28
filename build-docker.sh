#!/usr/bin/env bash

tag="v0.0.1"
docker build -t footprintai/fed-multimodal-restcol:${tag} -f dockerfile .
docker push footprintai/fed-multimodal-restcol:${tag}
