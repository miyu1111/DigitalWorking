from PIL import Image
import os
import sys

import pyocr
import pyocr.builders


from flask import Flask,render_template,request,redirect
app = Flask(__name__, static_folder='image')

class OcrText(object):
    def __init__(self):
        self.txt = ""
        self.words=[]
    def ex_text(self, image_id):
        # 1.インストール済みのTesseractのパスを通す
        path_tesseract = "C:\\Program Files\\Tesseract-OCR"
        if path_tesseract not in os.environ["PATH"].split(os.pathsep):
            os.environ["PATH"] += os.pathsep + path_tesseract
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit(1)

        tool = tools[0]
        print("Will use tool '%s'" % (tool.get_name()))

        self.txt = tool.image_to_string(
            Image.open(image_id),
            lang="eng",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )

        print( self.txt )
        #lines = self.txt.readlines()
        self.extract_words = []
        words = self.txt.split()
        for word in words:
            self.extract_words.append(word)


class DatabaseInit():
    db = []
    def __init__(self):
        pass

class DatabaseManager(DatabaseInit):
    def db_append(self,add_value):
        self.db.append(add_value)
    def db_get(self):
        return self.db
    def db_delete(self,value):
        self.db.pop(value)

class Dictionary(object):
    def __init__ (self):
        self.dic = {}
    def set_value(self):
        self.dic={'internet':"インターネット", 'of':"オブ", "thing":"ティング"}
        print(self.dic)


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'GET':
        ocr = OcrText()
        dic = Dictionary()
        db = DatabaseInit()
        if(os.path.exists("image/sample4.png")):
            return render_template('index.html')
        else:
            return render_template('index_noimage.html')
        
    if request.method == 'POST':
        dic = Dictionary()
        db_manage = DatabaseManager()
        if(not os.path.exists("image/sample4.png")):
            return render_template('index_init.html')
        ocr = OcrText()
        ocr.ex_text('image/sample4.png')

        #検索欄に何も入っていないなら、初期画面を表示させる
        #もしocrの結果と検索欄が異なっていたら、検索欄のほうを優先する
        num = request.form.get('comment')
        if num == None:
            return render_template('index_init.html')
        else:
            if num != ocr.txt:
                ocr.txt = num
        
        dic.set_value()
        return render_template('index.html', ocr_strings = ocr.txt, fruit = dic.dic)

@app.route('/image', methods=['POST'])
def image():
    if(not os.path.exists("image/sample4.png")):
        return render_template('index_noimage.html')
    ocr = OcrText()
    ocr.ex_text('image/sample4.png')
    return render_template('index_nodic.html', ocr_strings = ocr.txt)

@app.route('/reset', methods=['POST'])
def reset():
    return render_template('index_init.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port='5000',debug=True)