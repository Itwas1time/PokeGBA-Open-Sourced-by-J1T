#!/usr/bin/env python3

import os
import shutil
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


LAUNCHER_DIR = Path(__file__).resolve().parent
PROJECT_DIR = Path(os.environ.get('POKEMON_GBA_HOME', str(LAUNCHER_DIR.parent))).expanduser().resolve()
APP_DIR = PROJECT_DIR
MGBA = Path(os.environ.get('POKEMON_GBA_MGBA') or shutil.which('mgba-qt') or str(PROJECT_DIR / 'emulators' / 'mgba-qt')).expanduser()
ROM_DIR = Path(os.environ.get('POKEMON_GBA_ROM_DIR', str(PROJECT_DIR / 'roms'))).expanduser().resolve()
INFINITE_FUSION_DIR = Path(os.environ.get('POKEMON_GBA_FUSION_DIR', str(PROJECT_DIR / 'games' / 'Infinite Fusion'))).expanduser().resolve()
INFINITE_FUSION_EXE = INFINITE_FUSION_DIR / 'Game.exe'
WINE = Path(os.environ.get('POKEMON_GBA_WINE') or shutil.which('wine') or '/usr/bin/wine').expanduser()
WINE_PREFIX = Path(os.environ.get('POKEMON_GBA_WINEPREFIX', str(INFINITE_FUSION_DIR / 'wine-prefix'))).expanduser().resolve()
ICON_PATH = LAUNCHER_DIR / 'pokemon-gba-icon.png'
SPRITE_DIR = INFINITE_FUSION_DIR / 'Graphics/Battlers'


GAMES = (
    {
        'title': 'Pokémon Crystal',
        'filename': 'Pokemon - Crystal Version (USA).gbc',
        'art': 'crystal.png',
        'runner': 'mgba',
        'region': 'JOHTO',
        'system': 'GAME BOY COLOR',
        'year': '2001',
        'accent': '#79bfc0',
        'mascot': 150,
    },
    {
        'title': 'Pokémon Emerald',
        'filename': 'Pokemon - Emerald Version (USA, Europe).gba',
        'art': 'emerald.png',
        'runner': 'mgba',
        'region': 'HOENN',
        'system': 'GAME BOY ADVANCE',
        'year': '2005',
        'accent': '#74ba7b',
        'mascot': 384,
    },
    {
        'title': 'Pokémon LeafGreen',
        'filename': 'Pokemon - LeafGreen Version (USA, Europe).gba',
        'art': 'leafgreen.png',
        'runner': 'mgba',
        'region': 'KANTO',
        'system': 'GAME BOY ADVANCE',
        'year': '2004',
        'accent': '#a3c85f',
        'mascot': 3,
    },
    {
        'title': 'Pokémon Sapphire',
        'filename': 'Pokemon - Sapphire Version (USA, Europe).gba',
        'art': 'sapphire.png',
        'runner': 'mgba',
        'region': 'HOENN',
        'system': 'GAME BOY ADVANCE',
        'year': '2003',
        'accent': '#5e9fd1',
        'mascot': 382,
    },
    {
        'title': 'Pokémon Ultra Violet',
        'filename': 'Pokemon - Ultra Violet (v1.22).gba',
        'art': 'ultra-violet.png',
        'runner': 'mgba',
        'region': 'KANTO+',
        'system': 'GBA ROM HACK',
        'year': 'V1.22',
        'accent': '#a77ac7',
        'mascot': 151,
    },
    {
        'title': 'Pokémon Infinite Fusion',
        'filename': 'Game.exe',
        'art': 'infinite-fusion.png',
        'runner': 'wine',
        'region': 'FUSION LAB',
        'system': 'DESKTOP RPG',
        'year': '2024',
        'accent': '#da9064',
        'mascot': 6,
    },
)


# These sprites are used as little shelf decorations, not as status indicators.
SHELF_FRIENDS = (25, 133, 94, 6, 448, 130, 282, 257, 260, 384)


PAPER = '#f1e6cd'
PAPER_LIGHT = '#fff9e9'
PAPER_SHADOW = '#d7c49e'
INK = '#263d2d'
INK_SOFT = '#536552'
WOOD = '#815734'
WOOD_DARK = '#563920'
WOOD_LIGHT = '#a6784c'
GOLD = '#e2b64f'
RED = '#db5a4e'
GREEN = '#416d4b'
GREEN_DARK = '#294b35'
PLASTIC = '#b8b7ad'
PLASTIC_DARK = '#8e9088'
STAGE = '#132219'
STAGE_EDGE = '#2d4934'


class PokemonLauncher:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title('Pokémon Game Library')
        self.root.configure(bg=STAGE)
        self.root.geometry('1360x430')
        self.root.minsize(1100, 360)
        self.root.resizable(True, True)

        self.images = []
        self.cards = []
        self.selected_index = 0

        self._build_cartridge_row()
        self._bind_keyboard()
        self._center_window()
        self._select_game(0)
        self.root.after(80, self._focus_window)

    def _photo(self, path: Path, sample: int = 1):
        if not path.is_file():
            return None
        image = tk.PhotoImage(file=str(path))
        if sample > 1:
            image = image.subsample(sample, sample)
        self.images.append(image)
        return image

    def _build_cartridge_row(self) -> None:
        stage = tk.Frame(self.root, bg=STAGE, padx=18, pady=18)
        stage.pack(fill='both', expand=True)

        row = tk.Frame(stage, bg=STAGE)
        row.pack(expand=True)

        for index, game in enumerate(GAMES):
            shell = self._make_cartridge(row, index, game)
            shell.grid(row=0, column=index, padx=4, pady=4)
            self.cards.append((shell, shell))

    def _make_cartridge(self, parent: tk.Frame, index: int, game: dict):
        shell = tk.Frame(
            parent,
            bg=STAGE,
            padx=4,
            pady=4,
            highlightthickness=0,
        )

        cutout_name = game['art'].replace('.png', '-cutout.png')
        cartridge = self._photo(LAUNCHER_DIR / 'art/cartridges' / cutout_name, 6)
        if not cartridge:
            cartridge = self._photo(LAUNCHER_DIR / 'art/cartridges' / game['art'], 6)

        if cartridge:
            choice = tk.Button(
                shell,
                image=cartridge,
                command=lambda selected=index: self._launch_from_card(selected),
                bg=STAGE,
                activebackground=STAGE,
                relief='flat',
                bd=0,
                highlightthickness=0,
                cursor='hand2',
            )
        else:
            choice = tk.Button(
                shell,
                text=game['title'],
                command=lambda selected=index: self._launch_from_card(selected),
                font=('Sans', 10, 'bold'),
                fg=PAPER_LIGHT,
                bg=STAGE,
                activebackground=STAGE_EDGE,
                activeforeground=PAPER_LIGHT,
                relief='flat',
                bd=0,
                padx=12,
                pady=80,
                cursor='hand2',
            )
        choice.pack()

        for widget in (shell, choice):
            widget.bind('<Enter>', lambda event, selected=index: self._select_game(selected), add='+')
            widget.bind('<Button-1>', lambda event, selected=index: self._select_game(selected), add='+')
        return shell

    def _build_header(self) -> None:
        top_edge = tk.Frame(self.root, bg=GREEN_DARK, height=10)
        top_edge.pack(fill='x')
        top_edge.pack_propagate(False)

        header = tk.Frame(self.root, bg=PAPER, padx=34, pady=18)
        header.pack(fill='x')

        logo = tk.Canvas(
            header,
            width=62,
            height=62,
            bg=PAPER,
            highlightthickness=0,
        )
        logo.pack(side='left', padx=(0, 15))
        self._draw_pokeball(logo)

        copy = tk.Frame(header, bg=PAPER)
        copy.pack(side='left', anchor='w')
        tk.Label(
            copy,
            text='POKÉMON',
            font=('Sans', 10, 'bold'),
            fg=GREEN,
            bg=PAPER,
        ).pack(anchor='w')
        tk.Label(
            copy,
            text='Game Library',
            font=('Sans', 28, 'bold'),
            fg=INK,
            bg=PAPER,
        ).pack(anchor='w', pady=(0, 1))
        tk.Label(
            copy,
            text='Pick a cartridge and start your adventure.',
            font=('Sans', 11),
            fg=INK_SOFT,
            bg=PAPER,
        ).pack(anchor='w')

        friends = tk.Frame(header, bg=PAPER)
        friends.pack(side='right', anchor='s', padx=(10, 0))
        for index, sprite_id in enumerate(SHELF_FRIENDS):
            sprite = self._photo(SPRITE_DIR / str(sprite_id) / f'{sprite_id}.png', 6)
            if sprite:
                sticker = tk.Frame(
                    friends,
                    bg=PAPER_LIGHT if index % 2 else PAPER,
                    width=48,
                    height=54,
                )
                sticker.pack(side='left', padx=1)
                sticker.pack_propagate(False)
                tk.Label(sticker, image=sprite, bg=sticker['bg']).pack(side='top')

    def _draw_pokeball(self, canvas: tk.Canvas) -> None:
        canvas.create_oval(6, 6, 56, 56, fill=PAPER_LIGHT, outline=GREEN_DARK, width=2)
        canvas.create_arc(6, 6, 56, 56, start=0, extent=180, fill=RED, outline=GREEN_DARK, width=2)
        canvas.create_rectangle(7, 29, 55, 34, fill=GREEN_DARK, outline=GREEN_DARK)
        canvas.create_oval(21, 21, 41, 42, fill=GREEN_DARK, outline=GREEN_DARK)
        canvas.create_oval(26, 26, 36, 37, fill=PAPER_LIGHT, outline=PAPER_LIGHT)

    def _build_collage_banner(self) -> None:
        """A colorful Pokémon wall keeps the library from feeling like a blank UI."""
        banner = tk.Frame(self.root, bg=WOOD_DARK, padx=4, pady=4)
        banner.pack(fill='x', padx=28, pady=(0, 12))

        collage = tk.Canvas(
            banner,
            height=112,
            bg=GREEN,
            highlightthickness=0,
        )
        collage.pack(fill='x')
        collage.create_rectangle(0, 0, 1600, 112, fill=GREEN, outline=GREEN)
        collage.create_text(
            24,
            31,
            text='Choose your\nadventure',
            anchor='w',
            font=('Sans', 17, 'bold'),
            fill=PAPER_LIGHT,
        )
        collage.create_text(
            25,
            83,
            text='A collection of Pokémon stories',
            anchor='w',
            font=('Sans', 9),
            fill='#cfe3c4',
        )

        offsets = (7, -4, 9, -8, 4, -7, 8, -3, 7, -5)
        for index, sprite_id in enumerate(SHELF_FRIENDS):
            sprite = self._photo(SPRITE_DIR / str(sprite_id) / f'{sprite_id}.png', 4)
            if not sprite:
                continue
            x = 260 + index * 96
            y = 62 + offsets[index]
            circle_color = '#5b8c5c' if index % 2 else '#6b9962'
            collage.create_oval(x - 37, y - 37, x + 37, y + 37, fill=circle_color, outline='')
            collage.create_image(x, y, image=sprite)

    def _build_library_heading(self) -> None:
        heading = tk.Frame(self.root, bg=PAPER, padx=34, pady=0)
        heading.pack(fill='x', pady=(2, 10))

        tk.Frame(heading, bg=WOOD_LIGHT, height=2).pack(fill='x', side='bottom')
        copy = tk.Frame(heading, bg=PAPER)
        copy.pack(side='left', pady=(0, 8))
        tk.Label(
            copy,
            text='Your collection',
            font=('Sans', 16, 'bold'),
            fg=INK,
            bg=PAPER,
        ).pack(anchor='w')
        tk.Label(
            copy,
            text='Choose a case to play',
            font=('Sans', 9),
            fg=INK_SOFT,
            bg=PAPER,
        ).pack(anchor='w', pady=(2, 0))

        tk.Label(
            heading,
            text=f'{len(GAMES)} games',
            font=('Sans', 10, 'bold'),
            fg=INK_SOFT,
            bg=PAPER,
        ).pack(side='right', anchor='s', pady=(0, 8))

    def _launch_from_card(self, index: int) -> None:
        self._select_game(index)
        game = GAMES[index]
        self.launch((game['title'], game['filename'], game['runner']))

    def _build_footer(self) -> None:
        footer = tk.Frame(self.root, bg=PAPER, padx=34, pady=8)
        footer.pack(fill='x')
        tk.Frame(footer, bg=WOOD_LIGHT, height=2).pack(fill='x', side='top')
        tk.Label(
            footer,
            text='Arrow keys to browse  •  Enter to play  •  Esc to close',
            font=('Sans', 9),
            fg=INK_SOFT,
            bg=PAPER,
        ).pack(anchor='w', pady=(8, 0))

    def _bind_keyboard(self) -> None:
        self.root.bind('<Escape>', lambda event: self.root.destroy())
        self.root.bind('<Return>', lambda event: self._launch_selected())
        self.root.bind('<space>', lambda event: self._launch_selected())
        self.root.bind('<Right>', lambda event: self._move_selection(1))
        self.root.bind('<Left>', lambda event: self._move_selection(-1))
        self.root.bind('<Down>', lambda event: self._move_selection(4))
        self.root.bind('<Up>', lambda event: self._move_selection(-4))

    def _move_selection(self, delta: int) -> None:
        next_index = max(0, min(len(GAMES) - 1, self.selected_index + delta))
        self._select_game(next_index)

    def _select_game(self, index: int) -> None:
        self.selected_index = index
        for shell, _card in self.cards:
            shell.configure(bg=STAGE)

    def _launch_selected(self) -> None:
        game = GAMES[self.selected_index]
        self.launch((game['title'], game['filename'], game['runner']))

    def _focus_window(self) -> None:
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.root.attributes('-topmost', True)
        self.root.after(300, lambda: self.root.attributes('-topmost', False))

    def _center_window(self) -> None:
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = max(0, (screen_width - width) // 2)
        y = max(0, (screen_height - height) // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def launch(self, game: tuple[str, str, str]) -> None:
        title, filename, runner = game
        if runner == 'wine':
            executable = INFINITE_FUSION_EXE
            if not WINE.is_file():
                messagebox.showerror('Pokémon Game Library', f'Wine was not found at:\n{WINE}')
                return
            if not executable.is_file():
                messagebox.showerror('Pokémon Game Library', f'Infinite Fusion was not found at:\n{executable}')
                return
            command = [str(WINE), str(executable)]
            working_directory = INFINITE_FUSION_DIR
            environment = os.environ.copy()
            environment['WINEPREFIX'] = str(WINE_PREFIX)
        else:
            rom = ROM_DIR / filename
            if not MGBA.is_file():
                messagebox.showerror('Pokémon Game Library', f'mGBA was not found at:\n{MGBA}')
                return
            if not rom.is_file():
                messagebox.showerror('Pokémon Game Library', f'The ROM was not found:\n{rom}')
                return
            command = [str(MGBA), '-C', 'fullscreen=0', str(rom)]
            working_directory = APP_DIR
            environment = None

        try:
            subprocess.Popen(
                command,
                cwd=str(working_directory),
                env=environment,
                start_new_session=True,
            )
        except OSError as error:
            messagebox.showerror('Pokémon Game Library', f'Could not launch {title}:\n{error}')
            return
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    icon = tk.PhotoImage(file=str(ICON_PATH))
    root.iconphoto(True, icon)
    PokemonLauncher(root)
    root.mainloop()


if __name__ == '__main__':
    main()
