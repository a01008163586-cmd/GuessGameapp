[app]
title = SmartGuess
package.name = smartguess
package.domain = org.ahmedali
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
# ركز هنا، استخدم معمارية واحدة فقط
android.archs = arm64-v8a
android.accept_sdk_license = True
