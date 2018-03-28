from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
import tensorflow as tf
import sys
import traceback
import threading
#sound api
from playsound import playsound
#wikipedia api
import wikipedia as wiki

#google search api
from googlesearch import search

#PyQT UI elements
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

graph = tf.get_default_graph()
model = VGG16()

class PredictorThread(threading.Thread):
    def __init__(self,myapp,path):
        threading.Thread.__init__(self)
        self.myapp=myapp
        self.path=path
        
    def run(self):
        global graph,model
        with graph.as_default():
            image = load_img(self.path, target_size=(224, 224))
            image = img_to_array(image)
            image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
            image = preprocess_input(image)
            pred = model.predict(image)
            label = decode_predictions(pred)
            #print(label)
            label = label[0][0]
            self.myapp.Display_Title(label[1])
            #print('%s (%.2f%%)' % (label[1], label[2]*100))
            wiki_content=''
            try:
                info_page=wiki.page(label[1])
                img_content=info_page.content
                #print('------Wiki------')
                #print(img_content[:200]+'....')
                wiki_content=img_content[:350]+'....'
            except:
                tb = traceback.format_exc()
                print(tb)
                
            s_result=''
            #print('------Related----------')
            s=search(label[1],num=3,stop=1)
            for j in s:
                s_result=s_result+j+"\n"
                
            info = [label[1],wiki_content,s_result]
            self.myapp.Display(info)
            playsound(label[1]+".mp3")
        
        
qtCreatorFile = "pix.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.path=''
        self.upload.clicked.connect(self.Decode)
        #self.label.clicked.connect(self.Reload)
        #self.go.clicked.connect(self.Decode)
        
    def Decode(self):
        self.path=QFileDialog.getOpenFileName()[0]
        if(len(self.path)>1):
            self.upload.setStyleSheet("border-image: url"+"("+self.path+")")
            predictor_thread = PredictorThread(self,self.path)
            predictor_thread.start()
     
    #def Decode(self):
     #   self.upload.setStyleSheet("border-image: url"+"("+self.path+")")
        
    def Display(self,info):
        self.prediction.setText(info[0])
        self.wiki_holder.setText(info[1])
        self.search_holder.setText(info[2])
    def Display_Title(self,info):
        self.prediction.setText(info)
        
        
if __name__ == "__main__":
     app = QtWidgets.QApplication(sys.argv)
     window = MyApp()
     window.show()
     sys.exit(app.exec_())
    
        