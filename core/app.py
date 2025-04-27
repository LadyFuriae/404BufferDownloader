from core.adaptive_handling import download_adaptive_stream, combine, convert
from core.utilities import clear
from core.video_streams import get_video_streams, get_audio_streams
from core.metadata import get_metadata
from core.utilities import get_download_path
from core.video_streams import get_stream
import urllib.error
import urllib.request
import os
from pytubefix import YouTube
from pytubefix.exceptions import RegexMatchError, VideoUnavailable



def validate_url(url):
    try :
        YT = YouTube(url)
        YT.check_availability()
        return YT
    except (RegexMatchError, VideoUnavailable):
        print(f"\nError: Comprueba que sea un link Válido.\nVerifica que el video esté disponible en tu país, que no sea un LiveStream o que el vídeo no sea privado.\n")
        return None
    except Exception as e:
        print(f"\nError {e}. Comprueba que sea un link Válido.\n Verifica que el video esté disponible en tu país, que no sea un LiveStream o que el vídeo no sea privado.\n")   
        return None

def check_connection():
    try:
        urllib.request.urlopen("https://www.youtube.com", timeout=5)
        return True
    except urllib.error.URLError:
        return False


def show_resolution_and_codecs(streams):
    i = 1
    message = ""
    for stream in get_video_streams(streams):
        if stream.is_adaptive:
            message = "Adaptativo"
        else:
            message = "Progresivo"
        print(f"{i} Resolución: {stream.resolution} : Códec {stream.codecs} : Extensión {stream.subtype} : Tipo {message} : FPS {stream.fps}")
        i+=1

def show_audios(streams):
    i = 1
    bitrate_info = streams.abr if hasattr(streams, 'abr') and streams.abr is not None else 'N/A'
    sample_rate_info = f"{streams.audio_sample_rate} Hz" if hasattr(streams, 'audio_sample_rate') and streams.audio_sample_rate else 'N/A'
    for astream in get_audio_streams(streams):
        print(f"{i} Códec: {astream.codecs} : Bitrate: {bitrate_info} : Frecuencia: {sample_rate_info} Hz : Formato: {astream.mime_type}")
        i+=1

def select_video(streams):
    stream_list = list(streams)
    show_resolution_and_codecs(streams)
    election = int(input("Selecciona el vídeo que quieres descargar: "))
    return stream_list[election-1]

def select_audio(streams):
    astream_list = list(streams)
    show_audios(streams)
    election = int(input("Selecciona el audio que deseas descargar."))
    return astream_list[election-1]

def handle_adaptive(video, YT):
    video_path, audio_path = download_adaptive_stream(video, YT)
    if video_path and audio_path:
        print("¡Descarga exitosa!")
    print("Juntando audio y vídeo...")
    mkv = combine(video_path, audio_path)
    if mkv:
        print("¡Combinación de adio y vídeo extiosa!")
        election = int(input("¿Deseas convertir el vídeo a mp4 con códec H.264 mi causita?\n1. Sí\n2. No\nOpción: "))
        if election == 1:
            convert(mkv)
            os.remove(mkv)
        else: 
            return
    else:
        print("Hubo un error al intentar combinar audio y vídeo :c")
        return          
    try:
        clear(video_path, audio_path)
    except WindowsError:
        return



def ask_url():
    while True:
        url = str(input("Inserta la URL del vídeo que deseas descargar: "))
        if check_connection():
            print("Conexión establecida con Youtube.")
            YT = validate_url(url)
            if YT:
                meta = get_metadata(YT)
                if meta:
                    print("\nDatos del vídeo obtenidos correctamente\n")
                    for key, data in meta.items():
                        print(f"\n{key}: {data}")
                    break
                else:
                    print("Ocurrió un error al obtener los metadatos del vídeo.")
                    continue
            else:
                continue
        else:
            print("Hubo un error al intentar establecer la conexión con Youtube. Verifica tu conexión a internet y vuelve a intentarlo.")
            continue

    return YT        

def both(stream, YT):
    video = select_video(stream)
    print("Descargando...")
    if video.is_adaptive:
        handle_adaptive(video, YT)
    else:
        if video.download(get_download_path()):
            print("¡Descarga completada!")
        else:
            input("Error al descargar. Por favor, verfica tu conexión a internet e inténtalo de nuevo.")

def both_but_separate(stream, YT):
    just_video(stream)
    just_audio(YT)

def just_audio(YT):
    audio = YT.streams.get_audio_only()

    print("Descargando...")
    
    if audio.download(get_download_path()):
        print("¡Descarga completada!")
    else:
        input("Error al descargar. Por favor, verfica tu conexión a internet e inténtalo de nuevo.")
        

def just_video(stream):
    video = select_video(stream)
    print("Descargando...")
    if video.download(get_download_path()):
        print("¡Descarga completa!")
    else:
        input("Error al descargar. Por favor, verfica tu conexión a internet e inténtalo de nuevo.")

def menu():
    print("""1. Descargar video y audio (combinados)\n2. Descargar video y audio (separados)\n3. Descargar sólo vídeo.\n4. Descargar sólo audio.""")
    
def app():
    while True:

        YT = ask_url()
        stream = get_stream(YT)
        election = 0
        while True:
            menu()
            election = int(input("Opción: "))
            if election == 1:
                both(stream, YT)
                break
            elif election == 2:
                both_but_separate(stream, YT)
                break
            elif election == 3:
                just_video(stream)
                break
            elif election == 4:
                just_audio(YT)
                break
            else:
                print("Selecciona alguna de las 4 opciones disponibles.")
                continue
        try:
            election = int(input("1. Descargar nuevamente\n2. para salir."))
            if election == 1:
                continue
            else:
                break
        except Exception:
            break
            
