# Hướng dẫn chạy
1. Chạy trọng tài 
2. Lấy link trọng tài để chạy Backend và Frontend
3. Chạy Frontend 
4. Chạy Backend
5. Cách chạy cụ thể được hướng dẫn trong file README của referee, backend và frontend


# Cách chạy Backend

1. Vào thư mục /backend
2. cài đặt môi trường  `pip install -r requirements.txt`
3. Chạy `python app.py`
4. Điền thông tin phòng và 2 đội chơi
![Team 1](./images/team-1.png)
![Team 2](./images/team-2.png)

# Phương thức Utility và thuật toán tìm kiếm Threat space 

Bởi vì Gomoku (tiếng anh là: Tic Tac Toe Five In A Row) chạy rất chậm trên bảng lớn ( > 8x8 ), nếu chỉ chạy trên cách tính điểm của Utility thì sẽ chạy rất chậm, do đó dựa trên ý tưởng của thuật toán tìm kiếm threat space ( [Thread Space Search](https://www.baeldung.com/cs/gomoku-threat-space-search) và [Thread Space Search](https://github.com/HAnguyen-119/UET_AICaroGame/blob/master/backend/docs/allis_1994.pdf) ) cộng với việc giới hạn độ sâu của thuật toán minimax chỉ tính toán trên các ô lân cận (depth max = 3), việc này đã giảm kha khá thời gian chạy của code. Ngoài ra, để tối ưu thêm cho minimax thì việc sử dụng thêm Zobrist Hashing để lưu lại trạng thái của bàn cờ cũng như là lưu lại giá trị băm (hash_value) đã được tính trước đó của bàn cờ ( [Zobrist Hasing](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-5-zobrist-hashing/) ).

# [Project Assignment Report](https://docs.google.com/document/d/1xelg7x1IdE9ElLoozKewCNoRcbz2oX4GsviUYjBDmm0/edit?usp=drivesdk)
