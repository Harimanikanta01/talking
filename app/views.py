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