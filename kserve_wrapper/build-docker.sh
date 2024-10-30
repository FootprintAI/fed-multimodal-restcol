#!/usr/bin/env bash
#
TAG="v0.0.1.rc0"
docker build -t footprintai/fed-multimodal-restcol-kserve:${TAG} -f Dockerfile .
docker push footprintai/fed-multimodal-restcol-kserve:${TAG}
