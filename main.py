import flet as ft
import os

def main(page: ft.Page):
    # --- بخش دیباگ (برای فهمیدن نسخه Flet) ---
    flet_ver = getattr(ft, "__version__", "unknown")
    audio_exists = hasattr(ft, "Audio")
    
    page.title = "MostafaPlayer"
    page.padding = 10
    
    # نمایش وضعیت در بالای صفحه
    status_text = ft.Text(f"Flet: {flet_ver} | Audio: {audio_exists}", size=12, color=ft.colors.RED)
    msg_text = ft.Text("منتظر انتخاب فایل...", size=14)
    
    # --- تنظیمات Audio ---
    audio = None
    if audio_exists:
        try:
            audio = ft.Audio(src="", autoplay=False)
            page.overlay.append(audio)
        except Exception as e:
            msg_text.value = f"خطا در ایجاد Audio: {str(e)}"
    else:
        msg_text.value = "کلاس Audio در این نسخه یافت نشد!"

    # --- متدها ---
    def play_selected(e):
        if audio and e.control.data:
            audio.src = e.control.data
            audio.play()
            msg_text.value = f"درحال پخش: {os.path.basename(e.control.data)}"
            page.update()

    def on_files_picked(e: ft.FilePickerResultEvent):
        if e.files:
            container.controls.clear()
            for f in e.files:
                # ایجاد دکمه ساده بدون آیکن
                btn = ft.ElevatedButton(text=f.name, on_click=play_selected, data=f.path)
                container.controls.append(btn)
            msg_text.value = f"{len(e.files)} فایل انتخاب شد."
        page.update()

    # --- رابط کاربری ---
    picker = ft.FilePicker(on_result=on_files_picked)
    page.overlay.append(picker)
    
    container = ft.Column(scroll=ft.ScrollMode.AUTO, height=300)

    page.add(
        status_text,
        ft.ElevatedButton("انتخاب آهنگ", on_click=lambda _: picker.pick_files(allow_multiple=True)),
        msg_text,
        ft.Divider(),
        container
    )

ft.app(target=main)
