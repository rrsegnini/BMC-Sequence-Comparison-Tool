from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader, Context
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .lyrics.Lyrics import *
from .algorithms.AlineamientosP import *
from .lyrics.CompararCanciones import *
from django.template.loader import render_to_string


from .forms import NameForm


def get_songs(request):
    print("Song")

def search(request):
    artist1 = request.POST['artist1']
    song1 = request.POST['song1']

    artist2 = request.POST['artist2']
    song2 = request.POST['song2']

    Lyrics1 = get_lyrics(artist1, song1)
    Lyrics2 = get_lyrics(artist2, song2)

    txt_file1 = request.FILES.get('txt_file1', "")
    txt_file2 = request.FILES.get('txt_file2', "")

    percentage = float(request.POST['percentage'])
    segments = float(request.POST['segments'])

    if txt_file1:
        txt = txt_file1.read().decode("utf-8")
        txt = txt.replace('\n', '</br>')
        Lyrics1 = txt
        artist1 = "Unknown artist"
        song1 = "Unknown song"
    if txt_file2:
        txt = txt_file2.read().decode("utf-8")
        txt = txt.replace('\n', '</br>')
        Lyrics2 = txt
        artist2 = "Unknown artist"
        song2 = "Unknown song"

    start = time.time()
    res = alinearCanciones(Lyrics1, Lyrics2, percentage, segments)
    end = time.time()
    ElapsedTime = end - start
    print(res)
    SimilLyrics1 = []
    SimilLyrics2 = []
    if res != []:
        for element in res:
            SimilLyrics1 += [element[0]]
            SimilLyrics2 += [element[1]]
    else:
        SimilLyrics1 = ["No similarities were found :("]
        SimilLyrics2 = ""


    return render(request, 'main.html', {'Lyrics1': Lyrics1,
                                         'Lyrics2': Lyrics2,
                                         'artist':artist1,
                                         'song1':song1,
                                         'song2':song2,
                                         'artist2':artist2,
                                         'SimilLyrics1': SimilLyrics1,
                                         'SimilLyrics2': SimilLyrics2,
                                         'ElapsedTime': ElapsedTime})

def search2(request):


    artist2 = request.POST['artist2']


    artists2 = search_artist(artist2)

    #return render('main.html', {'artists2': artists}, context_instance=RequestContext(request))
    return render(request, 'main.html', {'artists2': artists2})

def main(request):

    #template = loader.get_template('main.html')
    return render(request, 'main.html')

def algorithms(request):
    return render(request, 'algorithms.html', {'match': 1,
                                               'mismatch': -1,
                                               'gap1': -2,
                                               'gap2':-2})

def exe_algorithms(request):
    # Si es 1 proviene del izquierdo.
    # Si es 3 proviene de arriba.
    # Si es 5 proviene del diagonal.
    # Si es 4 proviene de la izquierda y de arriba.
    # si es 6 proviene de la izquierda y de la diagonal.
    # si es 8 proviene de la arriba y de la diagonal.
    # si es 9 proviene de los tres lugares posibles.

    match = int(request.POST['match'])
    mismatch = int(request.POST['mismatch'])
    gap1 = int(request.POST['gap1'])
    gap2 = int(request.POST['gap2'])

    algo = request.POST['algorithms']

    str1 = request.POST['str1']

    str2 = request.POST['str2']

    txt_file1 = request.FILES.get('txt_file1', "")
    txt_file2 = request.FILES.get('txt_file2', "")

    if txt_file1:
        txt = txt_file1.read().decode("utf-8")
        txt = txt.replace('\n', '')
        str1 = txt
    if txt_file2:
        txt = txt_file2.read().decode("utf-8")
        txt = txt.replace('\n', '')
        str2 = txt

    matrix = []
    alignments = ""
    if algo == 'global':
        alignments, matrix = (alineamientoGlobal(str1, str2,match,mismatch,gap1,gap2))
    elif algo == 'local':
        alignments, matrix = (alineamientoLocal(str1, str2, match, mismatch, gap1, gap2))
    elif algo == 'semiglobal':
        alignments1, matrix = (alineamientoSemiglobal(str1, str2, 1, match, mismatch, gap1, gap2))
        alignments2, matrix = (alineamientoSemiglobal(str1, str2, 2, match, mismatch, gap1, gap2))
        alignments = alignments1 + alignments2




    return render(request, 'algorithms.html', {'matrix': matrix,
                                              'str1': str1,
                                              'str2': str2,
                                              'alignments': alignments,
                                               'match': match,
                                               'mismatch': mismatch,
                                               'gap1': gap1,
                                               'gap2': gap2})