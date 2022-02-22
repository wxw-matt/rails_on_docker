#!/bin/bash
TAG=$1
DOCKERFILE=$2

if [ "$DOCKERFILE" = "" ]; then
  DOCKERFILE="Dockerfile"
fi

if [ "$TAG" = "" ];then
  echo "Usage:"
  echo "\t sh buid.sh tag [dockerfile]\n"
  echo "\t tag        The tag for Docker image"
  echo "\t dockerfile The filename used as the Dockerfile, default is Dockerfile"
  exit 1;
fi

echo $TAG
echo $DOCKERFILE

ARCH=$(uname -m)
BUILDX=~/.docker/cli-plugins/docker-buildx
BUILDX_BUILDER=~/.docker/cli-plugins/.builder

if [ ! -f "$BUILDX" ]; then
  echo "Installing buildx ..."
  # Install buildx plugin for Docker
  curl -LO https://github.com/docker/buildx/releases/download/v0.7.1/buildx-v0.7.1.darwin-$ARCH
  mkdir -p ~/.docker/cli-plugins
  mv buildx-v0.7.1.darwin-$ARCH ~/.docker/cli-plugins/docker-buildx
  chmod a+x ~/.docker/cli-plugins/docker-buildx
fi

BUILDER_FOUND=`docker buildx ls | grep builder`
RESULT="$?"

if [[ ! -f "$BUILDX_BUILDER" && ! $RESULT = "0" ]]; then
  echo "Creating a new bulider ..."
  # Create a builder using specified image and driver
  docker buildx create --driver-opt image=moby/buildkit:master --name builder --driver docker-container --use
  docker buildx inspect --bootstrap

  # Set the  target platforms
  docker buildx create --platform linux/amd64
  docker buildx create --platform linux/arm64,linux/arm/v8
  echo "image:moby/buildkit:master" > $BUILDX_BUILDER
  echo "driver:docker-container" >> $BUILDX_BUILDER
fi

# Build image and push to Docker Hub, `docker login` is required beforehand.
docker buildx build --push -t $TAG --platform linux/amd64,linux/arm64 -f $DOCKERFILE .
