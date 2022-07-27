import requests
import json
import subprocess
import time
import sys
import threading
import pickle
import os
import platform
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QTextBrowser, QGridLayout, QGroupBox, QLabel, QMessageBox, QRadioButton)
import PyQt5.QtWidgets as qtwid
from PyQt5.QtCore import Qt
from function import (twitch_api, update, recorder)

client_id = "5ayor8kn22hxinl6way2j1ejzi41g2"
client_secret = "8tp18ssnpzbrzyyf0he83q3lsfayyx"

current_version = "1.1.0"

# streamer_list.pikle 파일이 없으면 생성
if not os.path.isfile("streamer_list.pickle"):
    with open("streamer_list.pickle", "wb") as f:
        pickle.dump([], f)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.createSetupGroup(), 0, 0)
        grid.addWidget(self.createTerminalGroup(), 1, 0)

        self.setLayout(grid)

        # self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('트위치 자동 녹화기 ' + current_version)
        self.resize(600, 400)
        self.show()

        try:
            self.access_token = twitch_api.get_access_token(client_id, client_secret)
            twitch_api.get_header(self.access_token)

        except:
            QMessageBox.information(self, "Error", "인터넷에 연결되어있지 않습니다.\n인터넷 연결을 확인해주세요.")
            exit()

        self.update_check()
        self.start_program()

    def createSetupGroup(self):
        groupbox = QGroupBox('설정')
        grid = QGridLayout()

        self.streamer_edit = qtwid.QLineEdit(self)
        self.save_btn = qtwid.QPushButton("추가",self)
        self.lbox_item = qtwid.QListWidget(self)

        self.streamer_edit.setToolTip('스트리머의 영문 닉네임을 입력하세요')
        self.title_label = QLabel("스트리머 영문 닉네임")

        grid.addWidget(self.radio_group(), 0, 0, 1, 2)
        grid.addWidget(self.title_label, 1, 0)
        grid.addWidget(self.streamer_edit, 2, 0)
        grid.addWidget(self.save_btn, 2, 1)
        grid.addWidget(self.lbox_item, 3, 0)
        grid.addWidget(self.btn_group(), 3, 1)

        self.save_btn.clicked.connect(self.Btn_addClick)        
        self.lbox_item.itemSelectionChanged.connect(self.Lbox_itemSelectionChange)

        groupbox.setLayout(grid)
        return groupbox

    def btn_group(self):
        groupbox = QGroupBox()
        grid = QGridLayout()

        self.btn_remove = qtwid.QPushButton("등록해제",self)
        grid.addWidget(self.btn_remove, 0, 0)
        self.btn_remove.clicked.connect(self.Btn_removeClick)
        self.btn_remove.setEnabled(False)

        groupbox.setLayout(grid)
        return groupbox
    
    def radio_group(self):
        groupbox = QGroupBox()
        grid = QGridLayout()

        self.radio_option1 = QRadioButton('스트리머 수동 등록', self)
        self.radio_option2 = QRadioButton('팔로우한 사람 등록', self)

        grid.addWidget(self.radio_option1, 0, 0)
        grid.addWidget(self.radio_option2, 0, 1)

        self.radio_option1.setChecked(True)
        self.radio_option1.clicked.connect(self.maunal_mode)
        self.radio_option2.clicked.connect(self.automatic_mode)

        groupbox.setLayout(grid)
        return groupbox

    def createTerminalGroup(self):
        groupbox = QGroupBox('로그')
        grid = QGridLayout()

        self.tb = QTextBrowser()
        grid.addWidget(self.tb, 0, 0)

        groupbox.setLayout(grid)

        return groupbox

    def console_print(self, message):
        date = "[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "]"
        self.tb.append(date + " " + message)

    def stream_check(self, streamer_id):
        headers = {'Client-ID': client_id, 'Authorization': 'Bearer ' + self.access_token}
        req = requests.get("https://api.twitch.tv/helix/streams?user_id=" + streamer_id, headers=headers)
    
        json_data = json.loads(req.text)
        #print(json_data)
        stream_status = json_data["data"]

        if not stream_status:
            return False
        else:
            return True
        
    def stream_record(self, streamer, streamer_id):
        if streamer_id == None:
            req = requests.get("https://api.twitch.tv/helix/users?login=" + streamer, headers={"Client-ID": client_id, "Authorization": "Bearer " + self.access_token})
            json_data = json.loads(req.text)
            streamer_id = json_data["data"][0]["id"]
        while True:
            if self.stream_check(streamer_id):
                self.console_print(streamer + "님 방송 녹화 시작")
                recorder.download_stream_legacy(streamer)
                self.console_print(streamer + "님 방송 녹화 종료")
            if not self.lbox_item.findItems(streamer, Qt.MatchExactly):
                break
            time.sleep(10)

    def start_program(self):
        self.console_print("프로그램 시작")

        with open("streamer_list.pickle", 'rb') as f:
            streamer_list = pickle.load(f)
            if streamer_list != []:
                self.console_print("스트리머 불러오기 완료")

                for streamer in streamer_list:
                    self.lbox_item.addItem(streamer)

                    threading.Thread(target=self.stream_record, args=(streamer, None), name=streamer).start()

    def update_check(self):
        # 업데이트 확인 코드
        try:
            latest_version = update.get_latest_version()
            if update.compare_version(current_version, latest_version):
                QMessageBox.information(self, "업데이트 알림", "현재 " + latest_version + " 버전이 사용가능합니다.\n업데이트 주소:\nhttps://github.com/dltkddnr04/Twitch-Auto-Recorder/releases")

        except:
            QMessageBox.information(self, "Error", "인터넷에 연결되어있지 않습니다.\n인터넷 연결을 확인해주세요.")

    def Btn_addClick(self):
        streamer = self.streamer_edit.text()
        if streamer == "":
            QMessageBox.information(self, "Error", "이름이 비어있습니다.")

        if self.radio_option1.isChecked():
            if self.lbox_item.findItems(streamer, Qt.MatchExactly):
                QMessageBox.information(self, "Error", "이미 등록된 스트리머입니다.")
                self.streamer_edit.setText("")
            else:
                self.add_streamer(streamer, None)

        else:
            # 경고창으로 물어보기
            if QMessageBox.question(self, "Warning", "기존의 모든 스트리머가 등록해제됩니다.\n 계속하시겠습니까?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                user = self.streamer_edit.text()
                req = requests.get("https://api.twitch.tv/helix/users?login=" + user, headers={"Client-ID": client_id, "Authorization": "Bearer " + self.access_token})
                json_data = json.loads(req.text)

                if len(json_data["data"]) == 0:
                    QMessageBox.information(self, "Error", "존재하지 않는 유저입니다.")
                else:
                    # lbox_item 전부 삭제하기
                    for i in range(self.lbox_item.count()):
                        self.lbox_item.takeItem(0)

                    streamer_list = []
                    with open("streamer_list.pickle", 'wb') as f:
                        pickle.dump(streamer_list, f)

                    self.streamer_edit.setText("")

                    self.console_print("전체 스트리머 등록 해제 완료")

                    user_id = json_data["data"][0]["id"]

                    req = requests.get("https://api.twitch.tv/helix/users/follows?from_id=" + user_id + "&first=100", headers={"Client-ID": client_id, "Authorization": "Bearer " + self.access_token})
                    json_data = json.loads(req.text)

                    follow_list = []
                    # follow_list에 스트리머 닉네임과 아이디 저장
                    for i in range(len(json_data["data"])):
                        follow_list.append([json_data["data"][i]["to_login"], json_data["data"][i]["to_id"]])

                    for streamer in follow_list:
                        if not self.lbox_item.findItems(streamer[0], Qt.MatchExactly):
                            self.add_streamer(streamer[0], streamer[1])

                    if not follow_list:
                        self.console_print("팔로우한 스트리머가 없습니다.")
                    else:
                        self.console_print("팔로우한 스트리머 등록 완료")
            else:
                QMessageBox.information(self, "Error", "취소되었습니다.")
            
            self.radio_option1.setChecked(True)
        return

    def add_streamer(self, streamer, streamer_id):
        if streamer_id == None:
            req = requests.get("https://api.twitch.tv/helix/users?login=" + streamer, headers={"Client-ID": client_id, "Authorization": "Bearer " + self.access_token})
            json_data = json.loads(req.text)

            if len(json_data["data"]) == 0:
                QMessageBox.information(self, "Error", "존재하지 않는 스트리머입니다.")
                return
            else:
                self.streamer_edit.setText("")
                streamer_id = json_data["data"][0]["id"]

        
        self.lbox_item.addItem(streamer)

        with open("streamer_list.pickle", 'rb') as f:
            streamer_list = pickle.load(f)
            
        streamer_list.extend(streamer.split())

        with open("streamer_list.pickle", 'wb') as f:
            pickle.dump(streamer_list, f)

        # 스레드 이름을 streamer_id로 설정
        threading.Thread(target=self.stream_record, args=(streamer, streamer_id), name=streamer).start()

        self.console_print(streamer + "님 등록 완료")
        return

    def Lbox_itemSelectionChange(self):        
        item = self.lbox_item.currentItem()
        if(item == None):
            self.btn_remove.setEnabled(False)
        else:
            self.btn_remove.setEnabled(True)

    def Btn_removeClick(self):
        selected_streamer = self.lbox_item.currentItem().text()

        with open("streamer_list.pickle", 'rb') as f:
            streamer_list = pickle.load(f)
        
        streamer_list.remove(selected_streamer.lower())

        with open("streamer_list.pickle", 'wb') as f:
            pickle.dump(streamer_list, f)

        self.radio_option1.setChecked(True)
        self.maunal_mode()

        self.lbox_item.takeItem(self.lbox_item.currentRow())
        self.console_print(selected_streamer + "님 등록해제 완료")
        return

    def maunal_mode(self):
        self.title_label.setText("스트리머 영문 닉네임")

    def automatic_mode(self):
        self.title_label.setText("본인의 영문 닉네임")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())