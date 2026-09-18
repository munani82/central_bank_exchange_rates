import os

def remove_startup_shortcut():
    app_data = os.environ.get("APPDATA")
    startup_dir = os.path.join(app_data, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    target_lnk = os.path.join(startup_dir, "CentralBankExchangeRateDashboard.lnk")
    
    if os.path.exists(target_lnk):
        try:
            os.remove(target_lnk)
            print("시작프로그램 바로가기 삭제 완료:", target_lnk)
        except Exception as e:
            print("삭제 실패:", e)
    else:
        print("시작프로그램에 등록된 바로가기가 없습니다.")

    # make_shortcut.vbs 임시파일도 정리
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vbs_path = os.path.join(base_dir, "make_shortcut.vbs")
    if os.path.exists(vbs_path):
        try:
            os.remove(vbs_path)
            print("임시 VBS 파일 삭제 완료")
        except Exception:
            pass

if __name__ == "__main__":
    remove_startup_shortcut()
