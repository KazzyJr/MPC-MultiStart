"""
Original code by: KazzyJr (c)2021
Latest revision: 30.01.2023
"""
import json
import os
import pathlib

__version__ = "1.0.3"

SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60
CONFIGURATION = {}
DEFAULT_START_TIME = "00:00:00"


class Time:
	"""Handles time differential calculation"""
	def __init__(self, given_time: str):
		"""
		Sets an internal reference time.
		:param given_time: A string representing the given start time in HH:MM:SS format
		"""
		hour, minute, seconds = given_time.split(":")
		self.hour = int(hour)
		if self.hour < 0:
			raise ValueError("Hours must be greater than or equal to 0")
		self.minute = int(minute)
		if self.minute < 0 or self.minute > 59:
			raise ValueError("Minutes range between 0-59")
		self.seconds = int(seconds)
		if self.seconds < 0 or self.seconds > 59:
			raise ValueError("Seconds range between 0-59")
		self.list = [self.hour, self.minute, self.seconds]

	string_condition: bool = False

	def calculate_time_span(self, time_difference: int) -> str:
		"""
		Calculates the time span using the time_difference. If the resulting time is out of bounds, defaults to
		the original time.
		"""
		total_seconds = self.hour * SECONDS_IN_HOUR + self.minute * SECONDS_IN_MINUTE + self.seconds
		target_time = total_seconds + time_difference
		self.hour = target_time//SECONDS_IN_HOUR
		self.minute = (target_time - self.hour * SECONDS_IN_HOUR)//SECONDS_IN_MINUTE
		self.seconds = target_time - self.hour * SECONDS_IN_HOUR - self.minute * SECONDS_IN_MINUTE
		self.list = [self.hour, self.minute, self.seconds]
		if target_time < 0:
			raise ValueError("Negative time")
		for index, item in enumerate(self.list):
			if 0 <= item < 10:
				item = f"0{str(item)}"
				self.list[index] = item
				self.string_condition = True
		if self.string_condition:
			self.string_condition = False
			return f"{self.list[0]}:{self.list[1]}:{self.list[2]}"
		else:
			return f"{self.hour}:{self.minute}:{self.seconds}"


class Movie:
	"""Handles movie objects."""
	all_movies = []

	def __init__(self, file_path: str, start_time: str = DEFAULT_START_TIME):
		"""
		Initializer for the movies. Sets all the values and remembers the instances.

		:param file_path: A path to the movie to be opened
		:param start_time: A string representing the initial start time in HH:MM:SS format
		"""
		self.file_path = file_path
		self.start_time = start_time
		self.new_start_time = ''
		Movie.all_movies.append(self)

	def __str__(self):
		return f'Movie located at: \n{self.file_path}\nhas an initial start time at {self.start_time} and an offset ' \
		       f'start time at {self.new_start_time}'


def load_configuration(config_path: str = 'config.json'):
	"""Global configuration object setting"""
	global CONFIGURATION
	config_text = pathlib.Path(config_path).read_text(encoding='utf-8')
	CONFIGURATION = json.loads(config_text)


def load_movies(json_path: pathlib.Path):
	"""Loads movies to the Movie class, keeping track of the instances"""
	movies_txt = json_path.read_text(encoding='utf-8')
	data = json.loads(movies_txt)
	for path, start_time in data.items():
		Movie(file_path=path, start_time=start_time)


def build_commands() -> list[str]:
	"""Calculates the time differentials and creates the command list"""
	all_commands = []
	for movie in Movie.all_movies:
		new_start_time = Time(movie.start_time).calculate_time_span(int(CONFIGURATION.get('time_offset')))
		movie.new_start_time = new_start_time
		cmd_complete = "{} \"{}\"{}{}{}".format(
				CONFIGURATION.get('base_command'),
				movie.file_path,
				CONFIGURATION.get('first_argument'),
				new_start_time,
				CONFIGURATION.get('second_argument')
		)
		all_commands.append(cmd_complete)
		if not CONFIGURATION.get("quiet"):
			print(movie)
	return all_commands


def start_execution(command_list: list[str]):
	"""Launches the MPC-HC processes"""
	if CONFIGURATION.get("dry_run"):
		for cmd in command_list:
			print(f'Would execute: cmd /c "{cmd}"')
	else:
		for cmd in command_list:
			os.system(f'cmd /c "{cmd}"')


if __name__ == "__main__":
	load_configuration()
	load_movies(pathlib.Path(CONFIGURATION.get('path_to_movies_json')))
	commands = build_commands()
	start_execution(commands)

