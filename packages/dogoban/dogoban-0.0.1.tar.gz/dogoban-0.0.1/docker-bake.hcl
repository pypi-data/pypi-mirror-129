target "docker-metadata-action" {
  context = "./"
  platforms = [
    "linux/amd64",
    "linux/arm64"
  ]
}

group "default" {
  targets = ["latest"]
}

target "latest" {
  inherits = ["docker-metadata-action"]
  target = "latest"
}

