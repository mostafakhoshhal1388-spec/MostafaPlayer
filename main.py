import flet as ft
import os


def safe_icon(name: str, fallback: str = "MUSIC_NOTE"):
    icons_obj = ft.icons
    if hasattr(icons_obj, name):
        return getattr(icons_obj, name)
    return getattr(icons_obj, fallback)


def create_audio():
    audio_cls = getattr(ft, "Audio", None)
    if audio_cls is None:
        return None

    try:
        return audio_cls(src="", autoplay=False)
    except Exception:
        return None


def main(page: ft.Page):
    page.title = "MostafaPlayer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 16

    playlist = []
    current_index = -1
    audio = create_audio()

    status_text = ft.Text(
        "برای شروع، فایل‌های MP3 را انتخاب کن.",
        size=14,
        weight=ft.FontWeight.BOLD,
    )

    playlist_view = ft.ListView(expand=True, spacing=6)

    def show_message(message: str):
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()

    if audio is not None:
        page.overlay.append(audio)
    else:
        status_text.value = "پخش صدا در این نسخه Flet در دسترس نیست."

    def update_playlist_view():
        playlist_view.controls.clear()
        for i, song_path in enumerate(playlist):
            song_name = os.path.basename(song_path)
            playlist_view.controls.append(
                ft.ListTile(
                    leading=ft.Icon(safe_icon("MUSIC_NOTE")),
                    title=ft.Text(song_name),
                    on_click=lambda e, idx=i: play_song(idx),
                )
            )

    def play_song(index: int):
        nonlocal current_index

        if audio is None:
            show_message("Audio در این نسخه پشتیبانی نمی‌شود.")
            return

        if index < 0 or index >= len(playlist):
            return

        current_index = index
        song_path = playlist[current_index]

        try:
            audio.src = song_path
            status_text.value = f"در حال پخش: {os.path.basename(song_path)}"
            page.update()
            audio.play()
        except Exception as ex:
            show_message(f"خطا در پخش: {ex}")

    def pause_song(e):
        if audio is None:
            return
        try:
            audio.pause()
        except Exception as ex:
            show_message(f"خطا در توقف: {ex}")

    def next_song(e):
        if not playlist:
            return
        play_song(current_index + 1)

    def prev_song(e):
        if not playlist:
            return
        play_song(current_index - 1)

    def set_volume(e):
        if audio is None:
            return

        value = float(e.control.value)
        try:
            if hasattr(audio, "set_volume"):
                audio.set_volume(value)
            elif hasattr(audio, "volume"):
                audio.volume = value
        except Exception as ex:
            show_message(f"خطا در تنظیم صدا: {ex}")

    def on_files_picked(e):
        playlist.clear()

        files = getattr(e, "files", None)
        if files:
            for file in files:
                file_path = getattr(file, "path", None)
                file_name = getattr(file, "name", "")

                if file_path and file_name.lower().endswith(".mp3"):
                    playlist.append(file_path)

        update_playlist_view()

        if playlist:
            status_text.value = f"{len(playlist)} آهنگ انتخاب شد."
        else:
            status_text.value = "هیچ فایل MP3 انتخاب نشد."

        page.update()

    picker = ft.FilePicker()
    picker.on_result = on_files_picked
    page.overlay.append(picker)

    page.add(
        ft.Column(
            [
                ft.Text("MostafaPlayer", size=26, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    "انتخاب آهنگ‌ها",
                    icon=safe_icon("AUDIO_FILE"),
                    on_click=lambda e: picker.pick_files(
                        allow_multiple=True,
                        allowed_extensions=["mp3"],
                    ),
                ),
                status_text,
                ft.Divider(),
                ft.Container(
                    content=playlist_view,
                    height=320,
                    padding=8,
                    border=ft.border.all(1, ft.colors.GREY_400),
                ),
                ft.Text("حجم صدا"),
                ft.Slider(
                    min=0,
                    max=1,
                    divisions=10,
                    value=0.8,
                    on_change=set_volume,
                ),
                ft.Row(
                    [
                        ft.IconButton(safe_icon("SKIP_PREVIOUS"), on_click=prev_song),
                        ft.IconButton(
                            safe_icon("PLAY_ARROW"),
                            on_click=lambda e: play_song(current_index if current_index != -1 else 0),
                        ),
                        ft.IconButton(safe_icon("PAUSE"), on_click=pause_song),
                        ft.IconButton(safe_icon("SKIP_NEXT"), on_click=next_song),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(),
                ft.Text("MostafaPlayer v1.0 | About / Support", size=10, italic=True),
            ]
        )
    )


ft.app(target=main)
