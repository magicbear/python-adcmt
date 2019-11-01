import adcmt

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

# adcmt.close(hDev)
# adcmt.end()