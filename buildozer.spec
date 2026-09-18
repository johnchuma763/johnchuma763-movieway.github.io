[app]
title = Movieway
package.name = movieway
package.domain = com.john.movieway
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png

android.api = 33
android.minapi = 21
android.build_tools = 33.0.2
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_agreement = True

[buildozer]
log_level = 2