import flet as ft
import os
from typing import List

# ---- Audio compatibility layer (old/new Flet) ----
def create_audio():
    """
    Tries to create an Audio control across different Flet versions.
    - Newer variants may have different modules.
    - Older variants expose ft.Audio
    """
    # 1) Try old API: ft.Audio
    AudioCls = getattr(ft, "Audio", None)
    if AudioCls is not None:
        try:
            return AudioCls(src="", autoplay=False)
        except Exception:
            pass

    # 2) Try newer API: flet.audio import Audio (some environments don't have it)
    try:
        from flet.audio import Audio  # type: ignore
        return Audio(src="", autoplay=False)
    except Exception:
        return None


def main(page: ft.Page):
    page.title = "MostafaPlayer"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 16

    playlist: List[str] = []
    current_index = -1

    # Create audio safely
    audio = create_audio()

    status_text = ft.Text("برای شروع، چند فایل MP3 انتخاب کنید.", size=14, weight=ft.FontWeight.BOLD)
    playlist_view = ft.ListView(expand=True, spacing=6, auto_scroll=False)

    def show_error(msg: str):
        page.snack_bar = ft.SnackBar(ft.Text(msg), open=True)
        page.update()

    # If audio is available, attach it
    if audio is not None:
        page.overlay.append(audio)
    else:
        show_error("پخش‌کننده صوت در این نسخه/محیط Flet در دسترس نیست. (Audio پشتیبانی نمی‌شود)")

    def play_song(index: int):
        nonlocal current_index
        if audio is None:
            show_error("Audio در این محیط در دسترس نیست.")
            return

        if 0 <= index < len(playlist):
            current_index = index
            song_path = playlist[current_index]

            # Some environments require file:// prefix, some accept raw path.
            # We try raw first; if it fails on your device, we can switch to file://.
            audio.src = song_path

            status_text.value = f"در حال پخش: {os.path.basename(song_path)}"
            page.update()

            try:
                audio.play()
            except Exception as ex:
                show_error(f"خطا در پخش فایل: {ex}")

    # ---- File picking (more reliable on Android than folder listing) ----
    def on_files_picked(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        playlist.clear()
        playlist_view.controls.clear()

        for idx, f in enumerate(e.files):
            # f.path should be a readable path in most cases
            path = getattr(f, "path", None)
            name = getattr(f, "name", None) or (os.path.basename(path) if path else "unknown")

            if path and name.lower().endswith(".mp3"):
                playlist.append(path)
                playlist_view.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.MUSIC_NOTE),
                        title=ft.Text(name),
                        on_click=lambda _, i=idx: play_song(i),
                    )
                )

        if playlist:
            status_text.value = f"{len(playlist)} آهنگ انتخاب شد. روی یکی کلیک کن."
        else:
            status_text.value = "هیچ فایل MP3 انتخاب نشد."

        page.update()

    picker = ft.FilePicker(on_result=on_files_picked)
    page.overlay.append(picker)

    # Volume control compatibility
    def set_volume(v: float):
        if audio is None:
            return
        # Some versions have volume property, some have set_volume method
        if hasattr(audio, "set_volume"):
            try:
                audio.set_volume(v)
                return
            except Exception:
                pass
        if hasattr(audio, "volume"):
            try:
                audio.volume = v
            except Exception:
                pass

    page.add(
        ft.Column(
            [
                ft.Text("MostafaPlayer", size=26, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    "انتخاب آهنگ‌ها (MP3)",
                    icon=ft.icons.AUDIO_FILE,
                    on_click=lambda _: picker.pick_files(
                        allow_multiple=True,
                        allowed_extensions=["mp3"],
                    ),
                ),
                status_text,
                ft.Divider(),
                ft.Container(content=playlist_view, height=320, border=ft.border.all(1, ft.colors.GREY_300), padding=8),
                ft.Slider(
                    min=0,
                    max=1,
                    divisions=10,
                    value=0.8,
                    label="حجم صدا",
                    on_change=lambda e: set_volume(float(e.control.value)),
                ),
                ft.Row(
                    [
                        ft.IconButton(ft.icons.SKIP_PREVIOUS, on_click=lambda _: play_song(current_index - 1)),
                        ft.IconButton(ft.icons.PLAY_ARROW, on_click=lambda _: play_song(current_index if current_index != -1 else 0)),
                        ft.IconButton(ft.icons.PAUSE, on_click=lambda _: audio.pause() if audio else None),
                        ft.IconButton(ft.icons.SKIP_NEXT, on_click=lambda _: play_song(current_index + 1)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(),
                ft.Text("MostafaPlayer | About/Support", size=10, italic=True),
            ]
        )
    )


ft.app(target=main)
