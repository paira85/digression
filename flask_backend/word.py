from flask import Blueprint, render_template
from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from googletrans import Translator  # Google Translator API

import fitz  # PyMuPDF
import os
import pypdfium2


app = Flask(__name__)
translator = Translator()

UPLOAD_FOLDER = 'C:/app/openai/transformer/uploads/pdf/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 업로드 폴더 생성 (없으면 생성)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

wordroute = Blueprint('wordroute', __name__)

@wordroute.route('/wordupload')
def huggingface_wordupload():
    return render_template('huggingface_wordupload.html')



@wordroute.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files['file']

    if pdf_file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        pdf_file.save(file_path)

    print(pdf_file)    
    print(file_path)

    text = ""
    text_array = []
    #PyMuPDF
    # reader = fitz.open(file_path) #PyMuPDF
    # for page_num in range(reader.page_count):
    #     page = reader.load_page(page_num)  # 페이지 로드
    #     text = page.get_text() + "\n "  # 텍스트 추출
    # reader.close()    

    #pdfReader    
    # reader = PdfReader(pdf_file)
    # for page in reader.pages:
    #     text = page.extract_text()

    #pypdfium2
    reader = pypdfium2.PdfDocument(file_path)

    # 현재 속성 확인 
    print(dir(reader))

    print('reader' , reader)
    # 페이지 수 확인
    num_pages = len(reader)
    print(f"총 {num_pages} 페이지가 있습니다.")

    # 모든 페이지에서 텍스트 추출
    for page_num in range(num_pages):
        # first_page = reader.get_page(page_num) 
        # print('first_page' , dir(first_page))
        # text = first_page.get_textpage()

        # 페이지 객체 생성
        page = reader[page_num]
        print(f"Page {page_num + 1}:")

        # 페이지의 텍스트 추출
        textpage = page.get_textpage()
        text = textpage.get_text_range()
        print(text)
        print("-" * 80)
        
    # PdfDocument 객체 닫기 
    print('text' , text)
    reader.close()
    return jsonify({"text": text})

@wordroute.route('/pdf_translate', methods=['POST'])
def pdf_translate():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input"}), 400

    translated_text = translator.translate(data['text'], src='ko', dest='en').text
    print(translated_text)
    return jsonify({"translated_text": translated_text})
