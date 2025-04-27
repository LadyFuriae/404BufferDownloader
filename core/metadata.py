from pytubefix import YouTube

def get_metadata(YT):
     try:
        metadata = {
                "Título": YT.title,
                "Canal": YT.author,
               
        }
        return metadata
     except Exception as e:
         print(f"\nError inesperado: {e}\n")
         return None
