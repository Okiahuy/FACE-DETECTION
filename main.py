import sys
import cv2
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QImage, QPixmap,QIcon
from PyQt5.uic import loadUi
from Gui import Ui_MainWindow


global_image = None

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.uic = Ui_MainWindow()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) 
        self.uic.setupUi(self)
        self.setFixedSize(717, 660)
        #sự kiện mở file
        self.uic.BTN_OPENFILE.clicked.connect(self.open_image)
        #sự kiện khi người dùng chọn thoát 
        self.uic.exitfrom.clicked.connect(self.confirm_exit)
        #sự kiện mở came
        self.uic.BTN_OPENCAME.clicked.connect(self.open_came)
        #sự kiện tắt camera
        self.uic.btn_turnoffcame.clicked.connect(self.stop_camera) 

        #sự khi khi nhấn phát hiện ở file 
        self.uic.btn_detetec_file.clicked.connect(self.detect_faces_file)
        #sự khi khi nhấn phát hiện ở file 
        self.uic.btn_detetec.clicked.connect(self.detect_faces_in_camera)
        
        self.capture = None

        self.uic.label1_COUNT_2.setStyleSheet("border: 2px solid black;")
        # Load the icon from the image file
        icon = QIcon("OpenCV_logo_no_text_.png")
        iconshutdow = QIcon("shut_dow.png")
        iconturnoffcame = QIcon("turnoff_came.png")

        # Set the icon for the button
        self.uic.exitfrom_2.setIcon(icon)
        self.uic.exitfrom.setIcon(iconshutdow)
        self.uic.btn_turnoffcame.setIcon(iconturnoffcame)
        
        self.uic.label1_COUNT_3.setStyleSheet("border: 2px solid black;")
        self.uic.label1_COUNT_4.setStyleSheet("background: white;")
        
        
        
    def open_came(self):
        if self.capture is None:
            self.capture = cv2.VideoCapture(0)
        while self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                self.uic.label1_COUNT_3.setPixmap(pixmap)
                self.uic.label1_COUNT_3.setScaledContents(True)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        self.capture.release()
        cv2.destroyAllWindows()
        
    def detect_faces_in_camera(self):
        if self.capture is None:  # Kiểm tra nếu capture là None
            reply = QMessageBox.question(self, 'Lỗi', 'Camera chưa được mở!', QMessageBox.Ok)
            return

        # Đường dẫn đến tệp XML của bộ phân loại khuôn mặt
        cascade_path = "haarcascade_frontalface_alt.xml"
        # Tạo một bộ phân loại khuôn mặt
        faceCascade = cv2.CascadeClassifier(cascade_path)
        
        self.capture = cv2.VideoCapture(0)
        
        detected_faces = 0  
        
        while True:  # Lặp để đọc khung hình từ camera
            ret, frame = self.capture.read()  # Đọc một khung hình từ camera
            if ret:  # Nếu việc đọc thành công
                # Phát hiện khuôn mặt trong hình ảnh
                
                # Chuyển đổi hình ảnh sang ảnh xám để tiện xử lý
                gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                faces = faceCascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=3)

                detected_faces = len(faces)  # Cập nhật số lượng khuôn mặt đã phát hiện

                # Vẽ hình chữ nhật xung quanh khuôn mặt được phát hiện
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Chuyển đổi hình ảnh đã vẽ khung sang QPixmap
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)

                # Hiển thị hình ảnh trên QLabel
                self.uic.label1_COUNT_3.setPixmap(pixmap)
                self.uic.label1_COUNT_3.setScaledContents(True)  # Thiết lập thuộc tính để tự động điều chỉnh kích thước

                # Hiển thị số lượng khuôn mặt được phát hiện lên label
                self.uic.label1_COUNT_5.setText(f"Số lượng khuôn mặt được phát hiện: {detected_faces}")

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Nếu người dùng nhấn phím 'q', thoát khỏi vòng lặp
                    break
            else:
                break

        self.capture.release()  # Giải phóng capture
        cv2.destroyAllWindows()  # Đóng tất cả các cửa sổ hiển thị



        
    def open_image(self):
        global global_image  # Khai báo biến toàn cục để lưu trữ dữ liệu hình ảnh
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if filename:
            global_image = cv2.imread(filename)  # Lưu trữ hình ảnh trong biến toàn cục
            if global_image is not None:  # Kiểm tra xem hình ảnh đã được tải thành công chưa
                # Chuyển đổi từ BGR sang RGB
                global_image = cv2.cvtColor(global_image, cv2.COLOR_BGR2RGB)
                # Lấy chiều cao, chiều rộng và số kênh màu của hình ảnh
                height, width, channel = global_image.shape
                # Tính số byte mỗi dòng của hình ảnh
                bytes_per_line = 3 * width
                # Tạo đối tượng QImage từ dữ liệu hình ảnh
                q_img = QImage(global_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                # Chuyển đổi QImage sang QPixmap
                pixmap = QPixmap.fromImage(q_img)
                # Đặt QPixmap vào QLabel để hiển thị hình ảnh
                self.uic.label1_COUNT_2.setPixmap(pixmap)
                # Thiết lập thuộc tính để tự động điều chỉnh kích thước của QLabel
                self.uic.label1_COUNT_2.setScaledContents(True)
                # Xóa bất kỳ văn bản hiển thị trước đó trên QLabel
                self.uic.label1_COUNT.setText("")
            else:
                # Hiển thị hộp thoại thông báo lỗi nếu không thể mở file hình ảnh
                reply = QMessageBox.question(self, 'Lỗi', 'Không thể mở file!', QMessageBox.Ok)


    def detect_faces_file(self):
        global global_image  # Truy cập biến toàn cục
        if global_image is not None:  # Kiểm tra xem ảnh đã được tải chưa
            # Đường dẫn đến tệp XML của bộ phân loại khuôn mặt
            cascade_path = "haarcascade_frontalface_alt.xml"
            # Tạo một bộ phân loại khuôn mặt
            faceCascade = cv2.CascadeClassifier(cascade_path)

            # Chuyển đổi hình ảnh sang ảnh xám để tiện xử lý
            gray_image = cv2.cvtColor(global_image, cv2.COLOR_BGR2GRAY)

            # Phát hiện khuôn mặt trong hình ảnh
            faces = faceCascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=3)

            # Đếm số lượng khuôn mặt đã phát hiện
            numbershow_faces = len(faces)

            # Nếu có ít nhất một khuôn mặt được phát hiện thì cho hiển thị số lượng 
            if numbershow_faces > 0:
                # Hiển thị số lượng khuôn mặt
                self.uic.label1_COUNT.setStyleSheet("color: rgb(0,170,0); ")
                self.uic.label1_COUNT.setText("Số lượng khuôn mặt được phát hiện:  " + str(numbershow_faces))

                # Vẽ hình chữ nhật xung quanh khuôn mặt được phát hiện
                for (x, y, w, h) in faces:
                    cv2.rectangle(global_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Hiển thị hình ảnh đã được nhận diện
                self.display_detected_image(global_image)
            else:
                # Hiển thị thông báo khi không phát hiện được khuôn mặt
                self.uic.label1_COUNT.setStyleSheet("color: red;")
                self.uic.label1_COUNT.setText("Không phát hiện được khuôn mặt!")
        else:
            # Hiển thị thông báo khi chưa có file ảnh nào được chọn
            reply1 = QMessageBox.question(self, 'Lỗi', 'Chưa có file ảnh nào được chọn!',  QMessageBox.Ok)

    def display_detected_image(self, image):
        if image is not None:  # Kiểm tra xem ảnh có khác None không
            # Chuyển đổi ảnh sang định dạng QImage
            height, width, channel = image.shape
            bytes_per_line = channel * width
            q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # Chuyển đổi QImage sang QPixmap
            pixmap = QPixmap.fromImage(q_img)
            
            # Đặt pixmap vào QLabel để hiển thị
            self.uic.label1_COUNT_2.setPixmap(pixmap)
            self.uic.label1_COUNT_2.setScaledContents(True)
        else:
            # Hiển thị hộp thoại thông báo lỗi nếu không có ảnh được phát hiện
            reply2 = QMessageBox.question(self, 'Lỗi', 'Không có ảnh được phát hiện!', QMessageBox.Ok)

        
      
    def stop_camera(self):
        if self.capture is not None:
            self.capture.release()
            self.capture = None 
        
        
    def confirm_exit(self):
        reply = QMessageBox.question(self, 'Confirm Exit', 'Bạn có chắc muốn thoát?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
