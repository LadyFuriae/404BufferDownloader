from pytubefix import streams

def get_stream(YT):
    return YT.streams

def get_video_streams(streams):
    video_streams = []
    for stream in streams.filter(type="video"):
        video_streams.append(stream)
    
    return video_streams

def get_audio_streams(streams):
    audio_streams = []
    for astream in streams.filter(type="audio"):
        audio_streams.append(astream)
    return audio_streams
