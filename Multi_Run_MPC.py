"""
Original code by: KazzyJr (c)2021
Latest revision: 06.09.2021
"""
import os
import sys


class Time:
	def __init__(self, given_time):
		hour, minute, seconds = given_time.split(":")
		self.hour = int(hour)
		self.minute = int(minute)
		self.seconds = int(seconds)
		self.list = [self.hour, self.minute, self.seconds]

	string_condition = 0

	def calculate_time_span(self, time_difference) -> str:
		total_seconds = self.hour * 3600 + self.minute * 60 + self.seconds
		target_time = total_seconds + time_difference
		self.hour = target_time//3600
		self.minute = (target_time - self.hour * 3600)//60
		self.seconds = target_time - self.hour * 3600 - self.minute * 60
		self.list = [self.hour, self.minute, self.seconds]
		if target_time < 0:
			raise ValueError("Negative time")
		for item in self.list:
			if 0 <= item < 10:
				temp_index = self.list.index(item)
				item = "0" + str(item)
				self.list[temp_index] = item
				self.string_condition = 1
		if self.string_condition == 1:
			self.string_condition = 0
			return f"{self.list[0]}:{self.list[1]}:{self.list[2]}"
		else:
			return f"{self.hour}:{self.minute}:{self.seconds}"


def main():

	time = sys.argv[1]

	for i in files_sync_time.values():
		end_time = Time(i).calculate_time_span(int(time))
		keys = list(files_sync_time.keys())
		values = list(files_sync_time.values())
		cmd_complete = base_command + " \"" + keys[values.index(i)] + "\"" + arguments + end_time
		os.system(f'cmd /c "{cmd_complete}"')


if __name__ == "__main__":
	# Populated with a direct path to a video and a target time from which we will add or subtract time
	files_sync_time = {
		"D:\\Videos\\Testing Video\\Placeholder.mp4": "00:15:00"
	}
	# MPC path
	base_command = "START \"C:\\Program Files (x86)\\K-Lite Codec Pack\\MPC-HC64\\\" mpc-hc64.exe"
	arguments = " /startpos "
	main()

