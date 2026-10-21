# Android build

The mobile shell builds as a static SvelteKit bundle and as an APK through
Tauri. Web build is verified in CI; APK build needs the Android SDK/NDK on the
machine.

```bash
npm ci
npm --prefix apps/mobile run check
npm --prefix apps/mobile run build
npm --prefix apps/mobile run tauri android init
npm --prefix apps/mobile run tauri android build -- --apk
```

Prerequisites (manual, Tauri docs): JDK 17+, Android SDK platform/build-tools,
NDK, `ANDROID_HOME`, and the Rust Android targets. This workspace has no
Android SDK, so `tauri android init` stops before generating
`src-tauri/gen/android`; H1.12's APK acceptance is verified on a machine with
the SDK.
