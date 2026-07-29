import flet as ft
import os

def main(page: ft.Page):
    page.title = "MostafaPlayer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # متغیرهای وضعیت
    playlist = []
    current_index = 0
    # اصلاح: قرار دادن مقدار "/" برای جلوگیری از خطا
    audio = ft.Audio(src="/", autoplay=False)
    page.overlay.append(audio)

    # المان‌های رابط کاربری
    status_text = ft.Text("لطفاً یک پوشه موزیک انتخاب کنید", size=16, weight=ft.FontWeight.BOLD)
    playlist_view = ft.ListView(expand=True, spacing=10)
    
    # تابع اجرای موزیک
    def play_song(index):
        nonlocal current_index
        if 0 <= index < len(playlist):
            current_index = index
            song_path = playlist[current_index]
            audio.src = song_path
            status_text.value = f"در حال پخش: {os.path.basename(song_path)}"
            page.update()
            audio.play()

    # مدیریت انتخاب پوشه
    def on_folder_picked(e: ft.FilePickerResultEvent):
        if e.path:
            playlist.clear()
            playlist_view.controls.clear()
            # لیست کردن فایل‌ها
            for file in os.listdir(e.path):
                if file.lower().endswith(".mp3"): # استفاده از lower برای شناسایی بهتر فرمت‌ها
                    full_path = os.path.join(e.path, file)
                    playlist.append(full_path)
                    playlist_view.controls.append(ft.ListTile(
                        leading=ft.Icon(ft.icons.MUSIC_NOTE),
                        title=ft.Text(file),
                        on_click=lambda _, i=len(playlist)-1: play_song(i)
                    ))
            page.update()

    folder_picker = ft.FilePicker(on_result=on_folder_picked)
    page.overlay.append(folder_picker)

    # چیدمان صفحه
    page.add(
        ft.Column([
            ft.Text("MostafaPlayer", size=30, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("انتخاب پوشه موزیک", icon=ft.icons.FOLDER_OPEN, 
                              on_click=lambda _: folder_picker.get_directory_path()),
            status_text,
            ft.Divider(),
            ft.Container(content=playlist_view, height=300),
            # اصلاح جزئی برای اسلایدر صدا که در فلت روی صدا تاثیر می‌گذارد
            ft.Slider(min=0, max=1, divisions=10, label="حجم صدا", on_change=lambda e: audio.set_volume(float(e.control.value))),
            ft.Row([
                ft.IconButton(ft.icons.SKIP_PREVIOUS, on_click=lambda _: play_song(current_index - 1)),
                ft.IconButton(ft.icons.PLAY_ARROW, on_click=lambda _: audio.play()),
                ft.IconButton(ft.icons.PAUSE, on_click=lambda _: audio.pause()),
                ft.IconButton(ft.icons.SKIP_NEXT, on_click=lambda _: play_song(current_index + 1)),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Text("MostafaPlayer v1.0 | حمایت از پروژه", size=10, italic=True)
        ])
    )

ft.app(target=main)
