from pytubefix import YouTube
import subprocess
import os
from core.utilities import get_download_path, download_with_progress

def download_adaptive_stream(video, YT):
    video_path = download_with_progress(video, get_download_path(), "Video", YT)
    audio_stream = YT.streams.get_audio_only()
    audio_path = download_with_progress(audio_stream, get_download_path(), "Audio", YT)

    if not video_path or not audio_path:
        input("Error al descargar. Por favor, verfica tu conexión a internet e inténtalo de nuevo.")
        return None, None
    return video_path, audio_path

def combine(video_path, audio_path):
    
    base_name = os.path.basename(video_path)
    root, ext = os.path.splitext(base_name)
    name = f"{root}_combined.mkv"
    path = os.path.join(get_download_path(), name)
    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    executable_path = os.path.join(main_dir, 'merge', 'ffmpeg.exe')

    command = [
        executable_path,
        "-y",
        "-i", audio_path,
        "-i", video_path,
        "-c:v", "copy",  
        "-c:a", "aac", 
        "-b:a", "320k",     
        "-ar", "48000", 
        "-f", "matroska",     
        path 
    ]

    print("\n--- Comando FFmpeg a ejecutar ---")
    print(command)
    print()

    try:
        subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
            encoding='utf-8'
        )
        return path
        
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg ha fallado (Código {e.returncode}):")
        print(e.stderr) 
        return None
    
def convert(mkv_video_path):
    name = os.path.basename(mkv_video_path)
    root, ext = os.path.splitext(mkv_video_path)

    if root.endswith('_combined'):
        root = root[:-len('_combined')]
    final_name = f"{root}_final.mp4"
    mp4_path = os.path.join(get_download_path(), final_name)

    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    executable_path = os.path.join(main_dir, 'merge', 'ffmpeg.exe')

    preset, crf = choose_command()
    print("Convirtiendo")
    command = [
        executable_path,
        "-y",                 
        "-i", mkv_video_path, 
        "-c:v", "libx264",   
        "-preset", preset,
        "-crf", crf,                                
        "-c:a", "copy",      
        "-f", "mp4",          
        mp4_path       
    ]

    try:
       
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            check=True,         
            text=True,          
            encoding='utf-8',   
            errors='replace'    
        )
        print(f"Conversión a MP4 (H.264) exitosa: {mp4_path}")
       
        return mp4_path

    except subprocess.CalledProcessError as e:
        
        print(f"FFmpeg (convert) ha fallado (Código {e.returncode}):")
        print("--- Salida de error de FFmpeg (convert) ---")
        print(e.stderr)
        print("--- Fin Salida de error ---")
        return None
    except FileNotFoundError:
        
        print(f"Error: No se encontró el ejecutable de FFmpeg.")
        print(f"Se intentó buscar en: {command[0]} (y posiblemente en el PATH)")
        print("Asegúrate de que FFmpeg esté instalado y accesible.")
        return None
    except Exception as e:
        
        print(f"Error inesperado durante la conversión: {e}")
        return None


def menu_command():
    print("Elije la calidad de la conversión:" )
    print("1. Máxima\n2. Alta. \n3. Media. \n4. Baja")
    
def choose_command():
    preset = ""
    crf = ""
    menu_command()
    election = int(input("Opción: "))

    if election == 1:
        preset = "slow"
        crf = "18"
    elif election == 2:
        preset = "medium"
        crf = "20"
    elif election == 3:
        preset = "fast"
        crf = "20"
    elif election == 4:
        preset = "veryfast"
        crf = "23"

    return preset, crf