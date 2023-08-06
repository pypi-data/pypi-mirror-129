import subprocess
from pathlib import Path
import shutil
from vinca.lib.vinput import VimEditor

vinca_path = Path(__file__).parent.parent.parent

path = Path(__file__).parent

# TODO rewrite without vim
def edit(card):
	front_path, back_path = (card.path/'front'), (card.path/'back')
	front = front_path.read_text()
	back = back_path.read_text()
	new_front = VimEditor(text = front, prompt = 'Q: ').run()
	front_path.write_text(new_front)
	new_back = VimEditor(text = back, prompt = 'A: ').run()
	for media in ('image_front', 'image_back', 'audio_front', 'audio_back'):
		media_file = card.path / media
		ref = VimEditor(prompt = f'select a file for {media}').run()
		if ref == 'delete' and media_file.exists():
			media_file.unlink()
		elif ref:
			source_file = Path.cwd() / ref
			assert source_file.exists(), f'{source_file} not found'
			shutil.copy(ref, media_file)

