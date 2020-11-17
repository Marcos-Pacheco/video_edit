import threading, io, sys
from pytube import YouTube
from pytube.cli import on_progress
from tqdm import tqdm
from time import sleep
from contextlib import redirect_stderr

def progress_callback(stream,chunks,bytes_remaining):
	total_size = stream.filesize
	bytes_downloaded = total_size - bytes_remaining

	"""
	V1 da função pbar
	"""
	# with tqdm(total=total_size, unit='b', unit_scale=True, ascii=True, miniters=10) as pbar:
	# 	pbar.set_description("Download ")
	# 	pbar.update(bytes_downloaded)

	"""
	V2 retirando a quebra de linha ou end of line
	"""
	f = io.StringIO()
	with redirect_stderr(f):
		with tqdm(total=total_size, unit='b', unit_scale=True, ascii=True) as pbar:
			pbar.set_description("Download ")
			pbar.update(bytes_downloaded)
		s = f.getvalue()

	# Retirna o END OF LINE do final da string
	s = s[:-1]
	sys.stdout.write(s)
	sys.stdout.flush()

	"""
	V3 retirando a quebra de linha ou end of line
	"""

	# if threading.active_count() > 0:
	# 	threads = threading.enumerate()
	# 	factory = TqdmMultiThreadFactory()
	#
	# 	for i, url in enumerate(threads, 1):
	#
	# 		f = io.StringIO()
	# 		with redirect_stderr(f):
	# 			with factory.create(i, total=total_size) as pbar:
	# 				# pbar.tqdm(total=total_size, unit='b', unit_scale=True, ascii=True)
	# 				# pbar.set_description("Download ")
	# 				pbar.update(bytes_downloaded)
	# 			s = f.getvalue()
	# 		# Retirna o END OF LINE do final da string
	# 		s = s[:-1]
	# 		sys.stdout.write(s)
	# 		sys.stdout.flush()


def finished_callback(stream,file_handle):
	nome = stream.title
	"""
	includes_audio_track
	includes_video_track
	"""
	if stream.includes_audio_track and stream.includes_video_track:
		print(f'{nome} baixado com sucesso.')
	elif stream.includes_audio_track:
		print(f'{nome} audio baixado com sucesso!')
	elif stream.includes_video_track:
		print(f'{nome} video baixado com sucesso!')

link = False
while link == False:
	try:
		link = str(input("Entre com o link do vídeo: "))
	except Exception as e:
		print(e,"valor não aceito, tente novamente.")

vid = YouTube(link)
vid.register_on_progress_callback(progress_callback)
vid.register_on_complete_callback(finished_callback)
vidinfo = vid.streams.order_by('resolution').desc()

# mostra todos os formatos disponíveis para download
for index,info in enumerate(vidinfo):
	print(index,info)

# selecione por id qual baixar
itag = False
while itag == False:
	try:
		itag = int(input('Digite a itag do video que deseja baixar: '))
	except Exception as e:
		print(e,"valor não aceito, tente novamente.")


"""
progressive = True - audio e video juntos
progressive = False - audio e video são separados
Se progressive == False baixar também o áudio
"""
selected = vid.streams.get_by_itag(itag)
path = './output'
filename = vid.title
if selected.is_progressive:
	selected.download(output_path=path,filename=filename+'_embeded')
else:
	print('Faixa de vídeo sem audio.')
	aud_list = vid.streams.filter(type='audio')
	for index,item in enumerate(aud_list):
		print(index,item)
	itag_aud = False
	while itag_aud == False:
		try:
			itag_aud = int(input('Digite a itag do áudio que deseja baixar: '))
		except Exception as e:
			print(e, "valor não aceito, tente novamente.")
	selected_aud = vid.streams.get_by_itag(itag_aud)
	job_thread1 = threading.Thread(target=selected.download, kwargs={'output_path':path, 'filename':filename+'_vid'})
	job_thread2 = threading.Thread(target=selected_aud.download, kwargs={'output_path':path,'filename':filename+'_aud'})
	job_thread1.start()
	job_thread2.start()