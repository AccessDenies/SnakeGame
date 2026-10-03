[app]

title = Snake Game
package.name = snakegame
package.domain = org.accessdenies

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

# API 34 is currently more stable with Buildozer than 35
android.api = 34
android.minapi = 24

# Added support for both 64-bit and 32-bit devices
android.archs = arm64-v8a, armeabi-v7a

android.allow_backup = True
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 0
