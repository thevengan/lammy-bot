from datetime import time

GUERRILLA_TIMESTAMPS = ["00:30", "02:30", "10:30", "12:30", "14:30", "16:30", "18:30", "20:30", "22:30"]
CONQUEST_TIMESTAMPS = ["01:30", "03:30", "08:30", "11:30", "13:30", "17:30", "19:30", "21:30", "23:30"]
PURIFICATION_TIMESTAMPS = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]

GUERRILLA_TIMES = [time(*map(int, timestamp.split(':'))) for timestamp in GUERRILLA_TIMESTAMPS]
CONQUEST_TIMES = [time(*map(int, timestamp.split(':'))) for timestamp in CONQUEST_TIMESTAMPS]
PURIFICATION_TIMES = [time(*map(int, timestamp.split(':'))) for timestamp in PURIFICATION_TIMESTAMPS]