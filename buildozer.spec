[app]
title = MyDatabaseApp
package.name = mydatabaseapp
requirements = python3, kivy==2.3.0, mysql-connector-python==8.0.33
version = 1.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
permissions = INTERNET
api = 34
archs = arm64-v8a, armeabi-v7a
sdk_path = /home/suvigyag/.buildozer/android/platform/android-sdk

