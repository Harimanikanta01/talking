from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
import requests
from googletrans import Translator
from gtts import gTTS
from django.http import FileResponse
from rest_framework.views import APIView
from io import BytesIO
# Create your views here.
import speech_recognition as sr
from pydub import AudioSegment
import pickle


class Pp(APIView):
     
     def post(self,request):
          name=request.data.get('name')
          l1=request.data.get('l1')
          l2=request.data.get('l2')
          t=Translator()
          ll=t.translate(name,src=l1,dest=l2)
          cc=ll.text
          print(cc)
          lba=gTTS(cc)
          
          
          mp3_fp = BytesIO()
          lba.write_to_fp(mp3_fp)
          mp3_fp.seek(0)
          


          return FileResponse(mp3_fp, as_attachment=True, filename="translation.mp3", content_type='audio/mpeg')
class Ha(APIView):
    def post(self, request):
        try:
            name = request.data.get("name")
            l1 = request.data.get("l1")
            l2 = request.data.get("l2")

            if not all([name, l1, l2]):
                return Response({"error": "Missing required fields."}, status=400)

            t = Translator()
            s1 = t.translate(name, src=l1, dest=l2)
            cc = s1.text

            return Response({"generated": cc})

        except Exception as e:
            return Response({"error": str(e)}, status=500)
class Pa(APIView):
    def post(self, request):
        file1 = request.FILES.get("file1")
        if not file1:
            return Response({"error": "No file uploaded"}, status=400)

        # Read uploaded file into memory
        mp3_data = file1.read()

        # Convert mp3 bytes to wav bytes using pydub and BytesIO
        mp3_audio = AudioSegment.from_file(BytesIO(mp3_data), format="webm")  # or "mp3" if mp3 format
        wav_io = BytesIO()
        mp3_audio.export(wav_io, format="wav")
        wav_io.seek(0)

        # Initialize recognizer
        reco = sr.Recognizer()

        
        with sr.AudioFile(wav_io) as source:
            audio_data = reco.record(source)
            try:
                text = reco.recognize_google(audio_data)
                print(text)
            except sr.UnknownValueError:
                text = "Could not understand audio"
            except sr.RequestError as e:
                text = f"Could not request results; {e}"
                print(text)
        return Response({"transcription": text})

class Ps(APIView):
    def post(self, request):
        movie_name = request.data.get("movie_name")  # Get movie from request body

        # Load data
        movies = pickle.load(open(r'C:\Users\ADMIN\Desktop\m27back\new\app\moviesupdated.pkl', 'rb'))

        similarity = pickle.load(open(r'C:\Users\ADMIN\Desktop\m27back\new\app\similarityupdated.pkl', 'rb'))

        # Check if movie exists
        if movie_name not in movies['title'].values:
            return Response({"error": f"Movie '{movie_name}' not found."})

        # Get index of the movie
        idx = movies[movies['title'] == movie_name].index[0]

        # Calculate similarity
        distances = list(enumerate(similarity[idx]))
        sorted_movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:5]

        # Build response
        recommendations = [movies.iloc[i[0]].title for i in sorted_movies]
        recommendations1 = [movies.iloc[i[0]].genre for i in sorted_movies]
        return Response({"recommendations": recommendations,"recommendations1":recommendations1})
