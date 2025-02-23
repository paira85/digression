# 설명: Hugging Face에서 제공하는 사전 학습된 번역 모델.

# 특징:

# 오픈소스 및 무료.
# 다양한 언어 쌍(한국어-영어 포함)을 지원.
# 로컬 환경에서 실행 가능.
# 사용법: Hugging Face Transformers 라이브러리를 사용하여 쉽게 실행할 수 있습니다.

#pip install transformers
#pip install sentencepiece


from flask import Flask, render_template, request, jsonify , make_response
from transformers import MarianMTModel, MarianTokenizer

from word import wordroute
from settlement import settlements 
app = Flask(__name__)

app.register_blueprint(wordroute)
app.register_blueprint(settlements)
# Use a pipeline as a high-level helper
#from transformers import pipeline

#pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-ko-en")
# Load model directly
#from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ko-en")
#model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ko-en")

# 번역 모델 로드
#model_name = "Helsinki-NLP/opus-mt-ko-en"
model_name = "./flask_backend/opus-mt-ko-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

model.eval()


def translate(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# 라우팅 설정
@app.route('/')
def index():
    return render_template('main.html')  # 메인 화면

# 메뉴바 
@app.route('/import_menu')
def import_menu():
    response = make_response(render_template('menu.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

    # return render_template('menu.html')

# 메뉴바 
@app.route('/import_footer')
def import_footer():
    return render_template('footer.html')  

# 번역기
@app.route('/translater')
def translater():
    return render_template('index.html')  # 메인 화면


@app.route('/translate', methods=['GET', 'POST'])
def translate_page():
    if request.method == 'POST':
        input_text = request.form.get('text')  # HTML 폼에서 입력 텍스트 가져오기
        translated_text = translate(input_text)
        return jsonify({"translated_text": translated_text})
    return render_template('translate.html')  # 번역 화면

if __name__ == '__main__':
    #app.run(host="127.0.0.1", debug=True,port=5001)
    # app.run(host="0.0.0.0", port=5000, debug=True)  # 127.0.0.1 대신 0.0.0.0 사용!
    app.run(host="192.168.45.218", port=5000, debug=True)  # 127.0.0.1 대신 0.0.0.0 사용!


# 그는 골칫덩어리야
# 103. 그걸 꼭 말로 해야 되니? 
# 104. 난 타고난 체질이야 
# 105. 정말 낭비야! 
# 106. 너 제정신이니? 
# 107. 너 뭔가 믿는 구석이 있구나
# 108. 이거 장난이 아닌데!  
# 109. 그냥 그렇다고 해, 뭘 자꾸 따져?  
# 110. 넌 왜 맨 날 그 모양이니? 
# 111. 뭐 이런 놈이 다 있어! 
# 112. 느낌이 오는데
# 113. 그는 자신감이 넘친다
# 114. 내가 만만하게 보여?