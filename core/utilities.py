import os
from tqdm import tqdm
from pytubefix import streams

def clear(video_path, audio_path):
    os.remove(video_path)
    os.remove(audio_path)

def get_download_path():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def download_with_progress(stream, output_path, descripcion, YT):
    total_size = stream.filesize
    
    # Crear barra de progreso
    with tqdm(
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        desc=descripcion,
        leave=True
    ) as pbar:
        # Función para actualizar la barra
        def on_progress(chunk, _, bytes_remaining):
            downloaded = total_size - bytes_remaining
            pbar.update(downloaded - pbar.n)
        
        # Registrar el callback en el objeto YouTube padre
        YT.register_on_progress_callback(on_progress)
        # Descargar el stream
        file_path = stream.download(output_path=output_path)
        
    return file_path


