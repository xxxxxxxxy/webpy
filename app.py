import web
import numpy as np
from keras.applications.densenet import preprocess_input
from keras.models import load_model
from keras.preprocessing import image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

render = web.template.render('templates/')
from web.template import ALLOWED_AST_NODES
ALLOWED_AST_NODES.append('Constant')

urls = (
    '/' , 'index' ,
    '/upload/(.*)', 'upload' ,
    '/(js|css|images|fonts|static)/(.*)', 'static',
    # '/showmeme' , 'showmeme',
    '/userupload' , 'userupload',
    '/uploadpage', 'uploadpage',
    # '/hello', 'hello'
    )
app = web.application(urls, globals())
model = load_model('model/de_model.h5')

class index:
    def GET(self):
        print('hey,I am here!')
        f = open('index.html', 'rb')
        return f

class uploadpage:
    def GET(self):
        return render.upload()
    def POST(self):
        x = web.input(myfile={})
        filedir = 'upload' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\', '/') # replaces the windows-style slashes with linux ones.
            filename="thisismy.jpg" # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        img = image.load_img('upload/thisismy.jpg', target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        y = model.predict(x)
        y = y.argmax(axis=-1)
        if y == 0:
            emotion = '负面'
        elif y == 1:
            emotion = '中立'
        elif y == 2:
            emotion = '负面'
        return render.result(emotion)

class userupload:
    def GET(self):
        return render.userupload()
    def POST(self):
        x = web.input(myfile={})
        filedir = 'static/usermemes' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filename=x.myfile.filename.replace('\\', '/') # replaces the windows-style slashes with linux ones.
            # filename="thisismy.jpg" # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        return render.userupload()
		
class static:
    def GET(self, media, file):
        try:
            f = open(media+'/'+file, 'r')
            return f.read()
        except:
            return '' # you can send an 404 error here if you want
            
            
class showmeme:
    def GET(self):
        return render.image()

# class uploadpage:
#     def GET(self):
#         return render.upload()
#     def POST(self):
#         print("aaaaaaaa")
#         i = web.input()
#         print(i.name)
#         return render.test(i.name)
#         # # line = i.decode('utf-8')
#         # img = image.load_img(imagePath, target_size=(224, 224))
#         # x = image.img_to_array(img)
#         # y = model.predict(x)
#         # return render.test(y)



if __name__ == "__main__":
    app.run()
