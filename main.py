import flet as ft
import os

def main(page: ft.Page):
    page.title = "MostafaPlayer"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    page.scroll = "auto"

    # لیست آهنگ‌ها (در نسخه بعدی انتخاب پوشه اضافه می‌شود)
    music_dir = "/storage/emulated/0/Music"
    songs = []
    
    if os.path.exists(music_dir):
        songs = [f for f in os.listdir(music_dir) if f.endswith(".mp3")]

    audio_player = None

    def play_song(e):
        nonlocal audio_player
        song_path = os.path.join(music_dir, e.control.data)
        
        # مدیریت پخش صدا با چک کردن پشتیبانی
        try:
            if hasattr(ft, "Audio"):
                if audio_player:
                    page.overlay.remove(audio_player)
                
                audio_player = ft.Audio(src=song_path, autoplay=True)
                page.overlay.append(audio_player)
                page.update()
                status_text.value = f"در حال پخش: {e.control.data}"
        except Exception as ex:
            status_text.value = f"خطا در پخش: {str(ex)}"
        page.update()

    # المان‌های رابط کاربری
    title_label = ft.Text("Mostafa Player", size=30, weight="bold", color="blue")
    status_text = ft.Text("آهنگی انتخاب نشده است", color="grey")
    
    song_list = ft.ListView(expand=1, spacing=10, padding=20)
    
    if not songs:
        song_list.controls.append(ft.Text("آهنگی در پوشه Music پیدا نشد."))
    else:
        for song in songs:
            song_list.controls.append(
                ft.ListTile(
                    title=ft.Text(song),
                    subtitle=ft.Text("برای پخش کلیک کنید"),
                    data=song,
                    on_click=play_song
                )
            )

    page.add(
        ft.Column(
            [
                title_label,
                status_text,
                ft.Divider(),
                song_list
            ],
            expand=True
        )
    )

ft.app(target=main)
