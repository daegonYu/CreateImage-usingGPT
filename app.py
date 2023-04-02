import os
import openai
from flask import Flask, redirect, render_template, request, url_for
import random
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
    funny_word = random.choice(["우끼끼","꼬물꼬물", "휘리릭", "쪼르륵", "콩닥콩닥", "바글바글", "도닥도닥", "촉촉", "쑥쑥", "슥슥", "와글와글", "둥실둥실", "찰랑찰랑", "우물쭈물"])

    if request.method == "POST":
        image_description = request.form["image_word"]
        trans_word = translator.translate(image_description, dest='en')
        emoji_word = f'Emphasize the lines and remove the color. cute and very simple messenger emoji like a roughly hand-drawn feel, meaning {trans_word.text}. background color is white. Print it in the center according to the size of the image.'
        # 캐리커쳐 느낌의, 대충 손으로 그린 추가하기 -> 별로 재미 없음
        # emoji_word = f'Draw simple and hand drawn caricature illustration meaning {trans_word.text}. Emphasize the lines and remove the color. cute and very simple messenger emoticon. background color is white. Print it in the center according to the size of the image.'
        # request.form -> 다음과 같은 딕셔너리 형태를 띔, ImmutableMultiDict([('image_word', '강아지')])
        print('프린트 :',request.form["image_word"], emoji_word) # 프린트 강아지

        response = openai.Image.create(
            prompt=emoji_word,
            n=1,
            size="256x256"
        )

        # print(response)
        result = response.data[0].url

        # 의성어 표현 -> 이해가 안되서 노잼
        # completion = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #             {"role": "system", "content": "You are the funniest man and the greatest comedian. Therefore, whatever I say, express it in one funny word. For example: Whoops!, Pungping, Hehe, Mmm"},
        #             {"role": "user", "content": f'{trans_word}'},
        #         ]
        # )

        # trans_word = translator.translate(completion.choices[0].message.content, dest='ko').text
        # print(trans_word)


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


    return render_template("index.html", result=result, funny_word=funny_word)

