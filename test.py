from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import sys
from PyQt6.QtGui import QPixmap, QImage, QPainter, QIcon
from PIL import Image
import cv2
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from rembg import remove
import shutil
import glob

os.makedirs('original', exist_ok = True)
os.makedirs('masked', exist_ok = True)
os.makedirs('latest_file', exist_ok = True)


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()
        self.bg_image_flag = 0
        self.frame_flag = 0
        self.bg_img_path = ""
        self.frame_path = ""
        self.img_counter = 1
        # self.background_img_idx = 0
        # self.frame_img_idx = 0
        # self.pixmap = QPixmap

    # def button_clicked(self):
    #     # checking if it is checked
    #     if self.r_b_1.isChecked():
    #         self.background_img_idx = 1
    #     elif self.r_b_2.isChecked():
    #         self.background_img_idx = 2
    #     print(self.background_img_idx)
    #
    #     # checking if it is checked
    #     if self.r_f_1.isChecked():
    #         self.frame_img_idx = 1
    #     elif self.r_b_2.isChecked():
    #         self.frame_img_idx = 2
    #     print(self.frame_img_idx)

    def initUI(self):
        self.setGeometry(100, 50, 791, 899)
        self.setWindowTitle("Virtual Photo Studio")
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 741, 251))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Background Image")
        self.browseBgImageButton = QtWidgets.QPushButton(parent=self.groupBox)
        self.browseBgImageButton.setGeometry(QtCore.QRect(50, 110, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.browseBgImageButton.setFont(font)
        self.browseBgImageButton.setObjectName("browseBgImageButton")
        self.browseBgImageButton.setText("Select Background Image")
        self.browseBgImageButton.clicked.connect(self.browse_background_image)
        self.bgImageGraphicsView = QtWidgets.QGraphicsView(
            parent=self.groupBox)
        self.bgImageGraphicsView.setGeometry(QtCore.QRect(420, 31, 291, 201))
        self.bgImageGraphicsView.setObjectName("bgImageGraphicsView")

        self.groupBox_2 = QtWidgets.QGroupBox(self)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 270, 741, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setTitle("Frame")
        self.browseFrameButton = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.browseFrameButton.setGeometry(QtCore.QRect(70, 100, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.browseFrameButton.setFont(font)
        self.browseFrameButton.setObjectName("browseFrameButton")
        self.browseFrameButton.setText("Select Frame")
        self.browseFrameButton.clicked.connect(self.browse_frame)
        self.frameGraphicsView = QtWidgets.QGraphicsView(
            parent=self.groupBox_2)
        self.frameGraphicsView.setGeometry(QtCore.QRect(420, 26, 291, 201))
        self.frameGraphicsView.setObjectName("frameGraphicsView")

        self.groupBox_3 = QtWidgets.QGroupBox(self)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 520, 741, 331))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setTitle("Capture Photo")
        self.captureImageButton = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.captureImageButton.setGeometry(QtCore.QRect(75, 100, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.captureImageButton.setFont(font)
        self.captureImageButton.setObjectName("captureImageButton")
        self.captureImageButton.setText("Capture Photo")
        self.captureImageButton.setDisabled(True)
        self.captureImageButton.clicked.connect(self.capture_image)
        self.outputImageGraphicsView = QtWidgets.QGraphicsView(
            parent=self.groupBox_3)
        self.outputImageGraphicsView.setGeometry(
            QtCore.QRect(420, 20, 291, 201))
        self.outputImageGraphicsView.setObjectName("outputImageGraphicsView")
        self.nameTextBox = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.nameTextBox.setGeometry(QtCore.QRect(10, 280, 211, 20))
        self.nameTextBox.setObjectName("nameTextBox")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(10, 260, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Name")
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(233, 260, 91, 16))
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Department")
        self.departmentTextBox = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.departmentTextBox.setGeometry(QtCore.QRect(230, 280, 141, 20))
        self.departmentTextBox.setObjectName("departmentTextBox")
        self.emailAddressTextBox = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.emailAddressTextBox.setGeometry(QtCore.QRect(380, 280, 231, 20))
        self.emailAddressTextBox.setObjectName("emailAddressTextBox")
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(380, 260, 101, 16))
        self.label_5.setObjectName("label_5")
        self.label_5.setText("Email Adress")
        self.sendImageButton = QtWidgets.QPushButton(parent=self.groupBox_3)
        self.sendImageButton.setGeometry(QtCore.QRect(620, 270, 101, 41))
        self.sendImageButton.setObjectName("sendImageButton")
        self.sendImageButton.setText("Send Photo")
        self.sendImageButton.clicked.connect(self.send_email)
        self.sendImageButton.setDisabled(True)

    def update(self):
        self.label.adjustSize()

    def browse_background_image(self):
        browse_file = QFileDialog.getOpenFileName(
            None, 'Choose Background', './Images/BG/', "Image files (*.jpg *.jpeg *.png *.gif)")[0]
        self.bg_img_path = browse_file
        if self.bg_img_path != '':
            print("Loading background image...")
            scene = QtWidgets.QGraphicsScene()
            pixmap = QPixmap(self.bg_img_path)
            pixmap = pixmap.scaledToWidth(270)  # resize the image canvas
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene.addItem(item)

            self.bgImageGraphicsView.setScene(scene)
            # self.originalImageGraphicsView.resize(pixmap.width()+10, pixmap.height()+10)

            # Enable segment button
            self.bg_image_flag = 1
            self.show_mixed_bg_frame()
            print("Done!")

    def browse_frame(self):
        browse_file = QFileDialog.getOpenFileName(
            None, 'Choose Frame', './Images/Frame/', "Image files (*.png)")[0]
        self.frame_path = browse_file
        if self.frame_path != '':
            print("Loading frame...")
            scene = QtWidgets.QGraphicsScene()
            pixmap = QPixmap(self.frame_path)
            pixmap = pixmap.scaledToWidth(270)  # resize the image canvas
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene.addItem(item)

            self.frameGraphicsView.setScene(scene)
            # self.originalImageGraphicsView.resize(pixmap.width()+10, pixmap.height()+10)

            # Enable segment button
            self.frame_flag = 1
            self.show_mixed_bg_frame()
            print("Done!")

    def capture_image(self):
        # cam = cv2.VideoCapture(3)
        cam = cv2.VideoCapture(1)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        # while cam.isOpened():
        cv2.namedWindow("Camera")
        print("Captured")

        while True:
            ret, frame = cam.read()

            if not ret:
                print("Failed to grab frame")
                break

            cv2.imshow("Camera", frame)

            k = cv2.waitKey(1)

            # if k % 256 == 27:  # ESC key to exit
            #     break
            # elif k % 256 == 32:  # Space key to capture image
            if k % 256 == 32:  # Space key to capture image
                img_name = "clicked0.png"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                cv2.destroyAllWindows()
                cam.release()

                # Save the original image
                original_filename = 'original/original_{}.png'.format(
                    self.img_counter)
                while os.path.exists(original_filename):
                    self.img_counter += 1
                    original_filename = 'original/original_{}.png'.format(
                        self.img_counter)

                img = Image.open(img_name)
                img.save(original_filename, format='png')

                # Remove the background
                masked_filename = 'masked/masked_{}.png'.format(
                    self.img_counter)
                while os.path.exists(masked_filename):
                    self.img_counter += 1
                    masked_filename = 'masked/masked_{}.png'.format(
                        self.img_counter)

                with open(masked_filename, 'wb') as f:
                    input_data = open(img_name, 'rb').read()
                    subject = remove(input_data, alpha_matting=True,
                                     alpha_matting_foreground_threshold=5)
                    f.write(subject)

                # Load the background image
                bg_img = Image.open(self.bg_img_path)
                bg_img = bg_img.resize((img.width, img.height))

                # Paste foreground onto the BG
                foreground_img = Image.open(masked_filename)
                bg_img.paste(foreground_img, (0, 0), foreground_img)

                # Load the frame image
                frame_img = Image.open(self.frame_path)
                # frame_img.show()
                # Ensure the foreground image has an alpha channel
                if 'A' not in frame_img.getbands():
                    frame_img.putalpha(255)  # Add a fully opaque alpha channel

                # # Calculate the position to paste the foreground image at the center
                # position = ((bg_img.width - frame_img.width) // 2, (bg_img.height - frame_img.height) // 2)

                bg_img.paste(frame_img, (0, 0), frame_img)

                # Save the result image
                self.bg_result_path = 'masked/bg_result{}.jpg'.format(
                    self.img_counter)
                while os.path.exists(self.bg_result_path):
                    self.img_counter += 1
                    self.bg_result_path = 'masked/bg_result{}.jpg'.format(
                        self.img_counter)

                # Convert the image to 'RGB' mode before saving as JPEG
                bg_img_rgb = bg_img.convert('RGB')
                bg_img_rgb.save(self.bg_result_path, format='jpeg')

                # # Save the latest result image in a separate folder
                # self.latest_bg_result_path = 'latest_file/bg_result.jpg'
                # shutil.copy(bg_result_path, self.latest_bg_result_path)

                # Display the result
                # cv2.imshow("Result", cv2.cvtColor(cv2.imread(latest_bg_result_path), cv2.COLOR_BGR2RGB))
                # cv2.waitKey(0)
                # cv2.imread('masked/bg_result4.jpg')
                cv2.destroyAllWindows()

                print("Process finished")

                self.img_counter += 1
                break

        scene = QtWidgets.QGraphicsScene()
        pixmap = QPixmap(self.bg_result_path)
        pixmap = pixmap.scaledToWidth(270)
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        scene.addItem(item)

        self.outputImageGraphicsView.setScene(scene)

        result_img = Image.open(self.bg_result_path)
        result_img.show()
        cv2.waitKey(0)

        self.sendImageButton.setDisabled(False)
        # print("loop exiting")
        # cam.release()
        # cv2.destroyAllWindows()
        # print("loop exiting successfully")

    def show_mixed_bg_frame(self):
        if self.bg_image_flag == 1 and self.frame_flag == 1:
            # Load the background image
            bg_img = Image.open(self.bg_img_path)
            # bg_img.show()

            # Load the frame image
            frame_img = Image.open(self.frame_path)
            # frame_img.show()
            # Ensure the foreground image has an alpha channel
            if 'A' not in frame_img.getbands():
                frame_img.putalpha(255)  # Add a fully opaque alpha channel

            # # Calculate the position to paste the foreground image at the center
            # position = ((bg_img.width - frame_img.width) // 2, (bg_img.height - frame_img.height) // 2)

            bg_img.paste(frame_img, (0, 0), frame_img)
            # bg_img.show("mixed image")

            bg_img.save("temp_bg.png")
            print("saved")

            scene = QtWidgets.QGraphicsScene()
            pixmap = QPixmap("temp_bg.png")
            pixmap = pixmap.scaledToWidth(270)  # resize the image canvas
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            scene.addItem(item)

            self.outputImageGraphicsView.setScene(scene)
            self.captureImageButton.setDisabled(False)
            print("done")

    # def mousePressEvent(self, event):
    #     print('mouse pressed ouside view')
    #     x = event.pos().x()
    #     y = event.pos().y()
    #     # pen = QPen(QtCore.Qt.black)
    #     # brush = QBrush(QtCore.Qt.black)
    #     # x = event.scenePos().x()
    #     # y = event.scenePos().y()
    #     print(x)
    #     # if self.opt == "Generate":
    #     #     self.addEllipse(x, y, 4, 4, pen, brush)
    #     # elif self.opt == "Select":
    #     #     print(x, y)

    def send_email(self):
        recipient_name = self.nameTextBox.text()
        recipient_email = self.emailAddressTextBox.text()
        recipient_department = self.departmentTextBox.text()

        if recipient_name and recipient_email and recipient_department:
            smtp_server = "smtp.gmail.com"
            port = 587  # For starttls
            sender_email = "Your Mail Address"
            password = "Security Code"

            # Create a multipart message
            message = MIMEMultipart()
            message['Subject'] = "Memories From CSE Fest"
            message['From'] = sender_email
            message['To'] = recipient_email

            # Add text content to the message
            text_content = f"Dear {recipient_name},\n\nThank you for being a part of our CSE Fest! We hope you have enjoyed the event as much as we did. As a token of appreciation, here is a memorable picture from the fest. Feel free to share it with your friends and relive the joyous moments.\n\nBest regards,\nVisual Machine Intelligence Lab (VMI Lab) \nand \nCSE Club of JUST\nDepartment of Computer Science and Engineering\nJashore University of Science and Technology."

            text_part = MIMEText(text_content)
            message.attach(text_part)

            # Attach the image
            with open(self.bg_result_path, 'rb') as image_file:
                image_part = MIMEImage(
                    image_file.read(), name=f"{recipient_name}.jpg")
                message.attach(image_part)

            # Create a secure SSL context
            context = smtplib.ssl.create_default_context()

            # Try to log in to the server and send the email
            try:
                server = smtplib.SMTP(smtp_server, port)
                server.ehlo()  # Can be omitted
                server.starttls(context=context)  # Secure the connection
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, message['To'], message.as_string())
                QMessageBox.about(
                    self, "Success", "Photo has been sent to your email. Thank you.")

                file_list = glob.glob('masked/bg_result*.jpg')
                file_list.sort(key=os.path.getmtime, reverse=True)
                if file_list:
                    # Get the path of the latest file
                    latest_file_path = file_list[0]
                    # Open and show the latest file
                    imgg = Image.open(latest_file_path)
                    save_path = f'latest_file/'
                    imgg.save(
                        save_path+f"{recipient_name.capitalize()+'_'+recipient_department.upper()}.jpeg", format='JPEG')
                    # imgg.show()

            except Exception as e:
                # Print any error messages to stdout
                print(e)
            finally:
                server.quit()
        else:
            QMessageBox.about(
                self, "Failed", "Please provide all the information")


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())


window()
