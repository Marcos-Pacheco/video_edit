import subprocess

"""
Aidiciona áudio a um vídeo que ainda não tenha faixa de áudio
"""
def ffmpeg_add_audio(video_path,audio_path):
    # with open(video_path) as file:
    #     video = file.read()
    # with open(audio_path) as file:
    #     audio = file.read()

    """
    primeiro loop tira o caminho acima
    """
    aux_index = 0
    for index,char in enumerate(video_path,-1):
        if char == ('/'):
            aux_index = index
    aux_filepath = video_path[aux_index+2:]

    """
    segundo loop retira o tipo de extensão do arquivo, restando apenas o nome do arquivo
    """
    for index,char in enumerate(aux_filepath):
        if char == '.':
            aux_index = index

    filename = aux_filepath[:aux_index]

    command = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c copy -shortest "C:/Users/Marcos Pachêco/Desktop/video_edit/output/{filename}_merged.mp4"'
    subprocess.check_output(command, shell=True)

ffmpeg_add_audio(str(input("Digite o caminho do vídeo: ")),str(input("Digite o caminho do áudio: ")))