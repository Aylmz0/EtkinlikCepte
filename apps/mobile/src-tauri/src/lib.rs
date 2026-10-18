//! EtkinlikCepte Mobile Shell — Tauri 2 entrypoint.
//! Owner: P6 (Abdullah Hilal).
//! Rust ceiling budget: < 200 lines (§4.4).

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|_app| {
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running EtkinlikCepte application");
}
