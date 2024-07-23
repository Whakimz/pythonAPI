from src import create_app

if __name__ == "__main__":
    """
    create_app().run(   # Run app
        debug=True,     # เปิดการแจ้งเตือนโค้ดผิดพลาด
        host='0.0.0.0', # ตั้งค่า Host
        port=81)        # Port ที่ต้องการระบุ
    """
    create_app().run(host='0.0.0.0', port=5001)
    # create_app().run(host='0.0.0.0', port=5001)
    # create_app().run(debug=True, host='0.0.0.0', ssl_context=context)