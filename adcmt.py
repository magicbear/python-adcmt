from ctypes import *
import ctypes

# ausb_lib = ctypes.CDLL("C:\\Program Files\\ADCMT\\USB Driver1.5.0e\\bin\\x64\\ausb.dll")
ausb_lib = ctypes.cdll.LoadLibrary("C:\\Program Files\\ADCMT\\USB Driver1.5.0e\\bin\\x64\\ausb.dll")

start = ausb_lib.ausb_start
# Timeout
start.argtypes = (ctypes.c_uint32,)
start.restype = ctypes.c_int

ausb_open = ausb_lib.ausb_open
ausb_open.argtypes = (ctypes.POINTER(ctypes.c_uint), ctypes.c_uint)
ausb_open.restype = ctypes.c_int

ausb_write64 = ausb_lib.ausb_write
ausb_write64.argtypes = (ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint)
ausb_write64.restype = ctypes.c_int

ausb_read64 = ausb_lib.ausb_read
ausb_read64.argtypes = (ctypes.c_uint, ctypes.c_char_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint))
ausb_read64.restype = ctypes.c_int

close = ausb_lib.ausb_close
close.argtypes = (ctypes.c_uint,)
close.restype = ctypes.c_int

end = ausb_lib.ausb_end
end.argtypes = None
end.restype = ctypes.c_int

clear = ausb_lib.ausb_clear
clear.argtypes = (ctypes.c_uint,)
clear.restype = ctypes.c_int

trigger = ausb_lib.ausb_trigger
trigger.argtypes = (ctypes.c_uint,)
trigger.restype = ctypes.c_int

readstb = ausb_lib.ausb_readstb
readstb.argtypes = (ctypes.c_uint, ctypes.POINTER(ctypes.c_int))
readstb.restype = ctypes.c_int

timeout = ausb_lib.ausb_timeout
timeout.argtypes = (ctypes.c_uint,)
timeout.restype = ctypes.c_int

local = ausb_lib.ausb_local
local.argtypes = (ctypes.c_uint,)
local.restype = ctypes.c_int

llo = ausb_lib.ausb_llo
llo.argtypes = (ctypes.c_uint,)
llo.restype = ctypes.c_int

reset = ausb_lib.ausb_reset
reset.argtypes = (ctypes.c_uint,)
reset.restype = ctypes.c_int

def open(MYID):
	hDev = ctypes.c_uint(0)
	rc = ausb_open(hDev, MYID)
	return (rc, hDev)

def write(hDev, strCmd):
	CmdCnt = len(strCmd)
	pBuffer = strCmd.encode("utf-8")
	return ausb_write64(hDev, pBuffer, CmdCnt)

def read(hDev, max_len = 256):
	buf = ctypes.create_string_buffer(max_len)
	pRead = ctypes.c_uint(0)
	print(buf)
	rc = ausb_read64(hDev, buf, max_len, pRead)
	return (rc, buf[:pRead.value])