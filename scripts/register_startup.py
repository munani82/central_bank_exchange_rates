import os
import subprocess

app_data = os.environ.get("APPDATA")
startup_dir = os.path.join(app_data, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bat_path = os.path.join(project_dir, "start_dashboard.bat")

vbs_content = f'''Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{startup_dir}\\CentralBankExchangeRateDashboard.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{bat_path}"
oLink.WorkingDirectory = "{project_dir}"
oLink.WindowStyle = 7
oLink.Save
'''

vbs_path = os.path.join(project_dir, "make_shortcut.vbs")
with open(vbs_path, "w", encoding="utf_8") as f:
    f.write(vbs_content)

res = subprocess.run(["cscript", "//nologo", vbs_path], capture_output=True, text=True)
print("VBScript 실행 결과 코드:", res.returncode)

target_lnk = os.path.join(startup_dir, "CentralBankExchangeRateDashboard.lnk")
if os.path.exists(target_lnk):
    print("시작프로그램 바로가기 생성 성공:", target_lnk)
else:
    print("바로가기 미생성")
