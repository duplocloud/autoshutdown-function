variable "TAG" {
    default = "1.0.0"
}

variable "REGISTRY" {
    default = "duplocloud"
}

variable "NAME" {
  default = "autoshutdown-function"
}

group "default" {
    targets = ["publish"]
}

target "publish" {
    tags = [
        "${REGISTRY}/${NAME}:latest",
        "${REGISTRY}/${NAME}:${TAG}"
    ]
    platforms = [
        "linux/amd64",
        "linux/arm64/v8"
    ]
}