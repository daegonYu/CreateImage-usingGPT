import os
import openai
from flask import Flask, redirect, render_template, request, url_for

import googletrans


app = Flask(__name__)

# key 보안 조심
openai.api_key = os.getenv("OPENAI_API_KEY")

# 번역기 구글 API 사용
translator = googletrans.Translator()


# flask run이라는 명령어를 통해 실행
@app.route("/", methods=("GET", "POST"))
def index():
    result = None
    mood_color = None

    if request.method == "POST":
        image_description = request.form["image_word"]
        trans_word = translator.translate(image_description, dest='en')
        emoji_word = f'Emphasize the lines and remove the color. cute and very simple messenger emoji like a roughly hand-drawn feel, meaning  {trans_word.text}. background color is white. Print it in the center according to the size of the image.'

        # request.form -> 다음과 같은 딕셔너리 형태를 띔, ImmutableMultiDict([('image_word', '강아지')])
        print('프린트',request.form["image_word"], emoji_word) # 프린트 강아지

        response = openai.Image.create(
            prompt=emoji_word,
            n=1,
            size="256x256"
        )

        print(response)
        result = response.data[0].url


        # 분위기에 맞는 컬러 설정 -> 색이 항상 같아서 취소
        # 구글 번역 API 
        
        # mood_color = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt="The CSS code for a color like a {}:\n\nbackground-color: #".format('cute '+trans_word.text),
        #     temperature=0,
        #     max_tokens=64,
        #     top_p=1.0,
        #     frequency_penalty=0.0,
        #     presence_penalty=0.0,
        #     stop=[";"]
        #     )
        # mood_color =  "#"+mood_color.choices[0].text
        # print('분위기 색:', mood_color)


    return render_template("index.html", result=result)

