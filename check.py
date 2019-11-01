import adcmt
import visa
import time

print("Initalize GPIB")
rm = visa.ResourceManager(visa_library="C:\\Windows\\SysWOW64\\visa32.Agilent Technologies - Keysight Technologies.dll")
rm.list_resources()

dev_3458a = rm.open_resource("GPIB0::22::INSTR")
dev_3458a.timeout = 8000

def read_3458():
	dev_3458a.write(" ")
	val1 = dev_3458a.read()[:-1].strip()

	dev_3458a.write(" ")
	fin_val = dev_3458a.read()[:-1].strip()
	return float(fin_val)

TMOUT = 3
MYID = 0
if (adcmt.start(TMOUT) != 0):
    print("開始できません")
    raise Exception("ERROR")

err, hDev = adcmt.open(MYID)
if err != 0:
	print("ターゲットをオープンできません")
	raise Exception("ターゲットをオープンできません")

if adcmt.write(hDev, "*IDN?") != 0:
	print("コマンドの送信に失敗しました")
	raise Exception("コマンドの送信に失敗しました")

err, buf = adcmt.read(hDev)
if err != 0:
	print("メッセージの受信に失敗しました")
	raise Exception("メッセージの受信に失敗しました")

print(buf)

check_list = [
	["SVR2", 30],
	["SVR3", 300],
	["SVR4", 3000],
	["SVR5", 30000]
]

for chk_range in check_list:
	adcmt.write(hDev, chk_range[0])
	time.sleep(0.1)
	adcmt.write(hDev, "OPR")
	time.sleep(0.1)
	for i in range(0, chk_range[1]+1, int(chk_range[1] / 20)):
		if i == 0:
			continue
		adcmt.write(hDev, "SOV +%.03f" % (i / 1000))
		time.sleep(0.05)
		print("SET %.07f READBACK %.07f" % (i / 1000, read_3458()))