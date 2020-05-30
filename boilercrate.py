# coding=utf-8

# Boilercrate 1.0
# Copyright 2020 Edvard Busck-Nielsen
#
#     Boilercrate is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Boilercrate is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Boilercrate.  If not, see <https://www.gnu.org/licenses/>.

import sys
import os


def show_help():
	print('Boilercrate')
	print('A tool for generating boilerplate code.')
	print('Usage:')
	print('\tboilercrate --option')
	print('\tor')
	print('\tboilercrate [Boiler name] --option')
	print('\tor')
	print('\tboilercrate [Boiler name] <target folder>')
	print('')
	print('Working with Boilers')
	print('\t[Boiler name] --add \t: create a new Boiler.')
	print('\t[Boiler name] --delete \t: delete a Boiler.')
	print('')
	print('Other')
	print('\t--list \t: show all available Boilers.')
	print('\t--help \t: show this menu.')
	print('')
	print('More information:')
	print('\tvisit: https://boilercrate.edvard.dev')


def list_boilers():
	possible_boilers = os.listdir(get_boiler_path('')[:-4])

	print('Boilers:')

	for possible_boiler in possible_boilers:
		if len(possible_boiler) >= 4:
			if possible_boiler[-4:] == '.zip':
				print('- ' + possible_boiler[:-4])


def boiler_exists(boiler_name):
	return os.path.isfile(get_boiler_path(boiler_name))


def get_boiler_path(boiler_name):
	from pathlib import Path
	return str(Path.home()) + '/.boilercrate/boilers/' + boiler_name + '.zip'


def delete_boiler(boiler_name):
	if boiler_exists(boiler_name):
		action = input('Are you sure you want to delete \"' + boiler_name + '\"? (y/N) ')
		if action.lower() == 'y':
			os.remove(get_boiler_path(boiler_name))
			print('\"' + boiler_name + '\" was deleted')


def new_boiler(boiler_name):
	import shutil

	if not boiler_exists(boiler_name):
		# Gets Boiler template.
		template_path = input('Boiler template folder path: ')

		if os.path.isdir(template_path):
			# Creates a .zip file from the template.
			# The last characters in the Boiler path is: ".zip" so they have to be removed.
			shutil.make_archive(get_boiler_path(boiler_name)[:-4], 'zip', template_path)
			print('Done! You can now generate this Boiler with: \"' + boiler_name + '\", it\'s safe to delete ' + template_path)
		else:
			print('Error! The template path is invalid!')

	else:
		print('Error! A boiler with the name \"' + boiler_name + '\" already exists!')


def generate_boiler(boiler_name, destination_path):
	import zipfile

	if boiler_exists(boiler_name) and os.path.exists(destination_path):
		# Checks if the destination is empty.
		if os.listdir(destination_path):
			action = input('The selected destination is not empy, it\'s content will be overwritten! Proceed? (y/N) ')

			if action.lower() != 'y':
				print('Canceled!')
				exit()

		# Extracts the Boiler to the user-selected path
		with zipfile.ZipFile(get_boiler_path(boiler_name)) as boiler_zip_file:
			boiler_zip_file.extractall(destination_path)

		print('The Boiler \"' + boiler_name + '\" has been constructed in: ' + destination_path)
	else:
		print('Error! Boiler \"' + boiler_name + '\" could not be found!')


def fallback():
	print('Please provide a Boiler name! You can view all available Boilers with the \"--list\" option')
	print('Use \"--help\" for more information.')


# Gets parameters and flags.
if len(sys.argv) >= 1:
	args = sys.argv[1:]

	options = []
	params = []

	# Separates out parameters and options (--[option]).
	for arg in args:
		if arg[0:2] == '--':
			options.append(arg)
			continue

		params.append(arg)

	if len(args) > 0 or len(params) > 0:
		if len(params):
			# Params where provided, and possible options too.
			requested_boiler_name = params[0]

			if '--add' in options:
				new_boiler(requested_boiler_name)

			if '--delete' in options:
				delete_boiler(requested_boiler_name)

			if len(params) >= 2:
				boiler_destination_path = params[1]

				# Assume boiler generation.
				generate_boiler(requested_boiler_name, boiler_destination_path)
		else:
			# No params where provided, only possible flags.
			if '--list' in options:
				list_boilers()

			if '--help' in options:
				show_help()

		exit()


# In case no/invalid arguments nor/or flags where given.
fallback()

