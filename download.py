from transformers import MarianMTModel, MarianTokenizer

# 모델 이름 지정
model_name = "Helsinki-NLP/opus-mt-ko-en"

# 토크나이저와 모델 다운로드
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

print("Model and tokenizer downloaded successfully!")
