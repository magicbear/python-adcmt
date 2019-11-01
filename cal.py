import adcmt
import visa
import time
import sys

print("Initalize GPIB")
rm = visa.ResourceManager(visa_library="C:\\Windows\\SysWOW64\\visa32.Agilent Technologies - Keysight Technologies.dll")
rm.list_resources()

dev_3458a = rm.open_resource("GPIB0::22::INSTR")
dev_3458a.timeout = 8000

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

def cal_cmd(hDev, cmd):
	adcmt.write(hDev, cmd)
	time.sleep(0.1)
	adcmt.write(hDev, "OPR")
	time.sleep(0.1)
	adcmt.write(hDev, "XM1")
	time.sleep(0.5)
	dev_3458a.write(" ")
	val1 = dev_3458a.read()[:-1].strip()
	time.sleep(0.1)
	dev_3458a.write(" ")
	fin_val = dev_3458a.read()[:-1].strip()
	adcmt.write(hDev, "XDT%s%.9E" % ("+" if float(fin_val) > 0 else "", float(fin_val)))
	time.sleep(0.1)
	return float(fin_val)

# GO Into CALIBRATION MODE
adcmt.write(hDev, "CAL1")
time.sleep(0.1)
print("Start CALIBRATION Voltage Source")
time.sleep(0.1)
adcmt.write(hDev, "XF0")
time.sleep(0.1)
adcmt.write(hDev, "XCLR")
time.sleep(0.1)
vol_cal = ["XR2", "XR3", "XR4", "XR5"]
for cal_range in vol_cal:
	adcmt.write(hDev, cal_range)
	time.sleep(0.1)
	print("CALIBRATION RANGE %s +" % (cal_range))
	adcmt.write(hDev, "XS0")
	time.sleep(0.1)
	adcmt.write(hDev, "XS?")
	err, buf = adcmt.read(hDev)
	if buf.decode("utf-8").strip() == "XS 0":
		print("  CALIBRATION Zero Point: ", end="")
		print("%.07f" % (cal_cmd(hDev, "XN0")))

		print("  CALIBRATION Full Scale: ", end="")
		print("%.07f" % (cal_cmd(hDev, "XN1")))
	else:
		print("ERROR STATE")
		break

	print("CALIBRATION RANGE %s -" % (cal_range))
	adcmt.write(hDev, "XS1")
	time.sleep(0.1)
	adcmt.write(hDev, "XS?")
	err, buf = adcmt.read(hDev)
	if buf.decode("utf-8").strip() == "XS 1":
		print("  CALIBRATION Zero Point: ", end="")
		print("%.07f" % (cal_cmd(hDev, "XN0")))

		print("  CALIBRATION Full Scale: ", end="")
		print("%.07f" % (cal_cmd(hDev, "XN1")))
	else:
		print("ERROR STATE")
		break

# adcmt.write(hDev, "SBY")
# print("Start CALIBRATION Current Source, Please change DMM to current mode and press ENTER")
# time.sleep(0.1)
# sys.stdin.readline()

# adcmt.write(hDev, "XF1")
# time.sleep(0.1)
# adcmt.write(hDev, "XCLR")
# time.sleep(0.1)

# vol_cal = ["XR1", "XR2", "XR3"]
# for cal_range in vol_cal:
# 	adcmt.write(hDev, cal_range)
# 	time.sleep(0.1)
# 	print("CALIBRATION RANGE %s +" % (cal_range))
# 	adcmt.write(hDev, "XS0")
# 	time.sleep(0.1)
# 	adcmt.write(hDev, "XS?")
# 	err, buf = adcmt.read(hDev)
# 	if buf.decode("utf-8").strip() == "XS 0":
# 		print("  CALIBRATION Zero Point: ", end="")
# 		print("%.07f" % (cal_cmd(hDev, "XN0")))

# 		print("  CALIBRATION Full Scale: ", end="")
# 		print("%.07f" % (cal_cmd(hDev, "XN1")))
# 	else:
# 		print("ERROR STATE")
# 		break

# 	print("CALIBRATION RANGE %s -" % (cal_range))
# 	adcmt.write(hDev, "XS1")
# 	time.sleep(0.1)
# 	adcmt.write(hDev, "XS?")
# 	err, buf = adcmt.read(hDev)
# 	if buf.decode("utf-8").strip() == "XS 1":
# 		print("  CALIBRATION Zero Point: ", end="")
# 		print("%.07f" % (cal_cmd(hDev, "XN0")))

# 		print("  CALIBRATION Full Scale: ", end="")
# 		print("%.07f" % (cal_cmd(hDev, "XN1")))
# 	else:
# 		print("ERROR STATE")
# 		break

print("Write DATA TO MEMORY")
adcmt.write(hDev, "XWR")
time.sleep(0.1)
# GO Into CALIBRATION MODE
adcmt.write(hDev, "CAL0")
time.sleep(0.1)
