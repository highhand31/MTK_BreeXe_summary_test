from ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow,QApplication
import qdarkstyle
from qdarkstyle.light.palette import LightPalette
import sys,json,dotenv

class AppWindow(QMainWindow):
    def __init__(self):
        #----init UI
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.keys = ['article','short','summary']

        #----read the data
        self.path = env['PATH']

        self.loadTechData()
        #----events
        self.ui.listWidget_titles.clicked.connect(
            self.listWidget_titles_clicked
        )
        self.ui.listWidget_titles.currentItemChanged.connect(
            self.listWidget_titles_clicked
        )

    def listWidget_titles_clicked(self):
        current_item = self.ui.listWidget_titles.currentItem()
        if current_item is not None:
            title = current_item.text()

            if isinstance(self.content.get(title),dict):
                data_dict = self.content[title]
                for key in self.keys:
                    if data_dict.get(key) is not None:
                        if key == 'article':
                            self.ui.textEdit_article.setText(data_dict[key])
                            self.ui.label_words_sum_article.setText(f"字數:{len(data_dict[key])}")
                        elif key == 'short':
                            d = data_dict[key]['Breexe']
                            self.ui.textEdit_short_Breexe.setText(d)
                            self.ui.label_words_short_Breexe.setText(f"字數:{len(d)}")

                            d = data_dict[key]['gpt-3.5-turbo-0125']
                            self.ui.textEdit_short_gpt.setText(d)
                            self.ui.label_words_short_gpt.setText(f"字數:{len(d)}")
                        elif key == 'summary':
                            d = data_dict[key]['Breexe']
                            self.ui.textEdit_sum_Breexe.setText(d)
                            self.ui.label_words_sum_Breexe.setText(f"字數:{len(d)}")

                            d = data_dict[key]['gpt-3.5-turbo-0125']
                            self.ui.textEdit_sum_gpt.setText(d)
                            self.ui.label_words_sum_gpt.setText(f"字數:{len(d)}")

    def loadTechData(self):

        pipes = dict(
            read_title_links=self.read_titles,
            display_titles=self.show_titles,
            # read_content=self.read_content_tabTechNews,
            # read_summary=self.read_summary_tabTechNews,
        )

        for name, method in pipes.items():
            st = True
            msg = ""
            try:
                method()
            except Exception as err:
                st = False
                msg = f"Error in {name}: {str(err)}"


            if st is False:
                print(msg)

    def read_titles(self):
        with open(self.path,'r') as f:
            self.content = json.load(f)
        self.titles = self.content.keys()

    def show_titles(self):
        self.ui.listWidget_titles.clear()
        self.ui.listWidget_titles.addItems(self.titles)


if __name__ == "__main__":
    env = dotenv.dotenv_values()
    app = QApplication(sys.argv)
    w = AppWindow()

    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5', palette=LightPalette()))
    w.show()
    sys.exit(app.exec_())