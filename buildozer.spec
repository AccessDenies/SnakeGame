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

android.api = 35
android.minapi = 23
android.archs = arm64-v8a

android.allow_backup = True
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 0
