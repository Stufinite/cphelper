#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
import re, jieba, pyprind, pymongo, json
from timetable.models import Course
from collections import defaultdict

class Command(BaseCommand):
	help = 'Convenient Way to insert Intern of Yourator json into arrogant'
	client = pymongo.MongoClient(None)
	db = client['timetable']
	Genra = db['Genra']
	CourseOfDept = db['CourseOfDept']
	CourseOfTime = db['CourseOfTime']
	genra = None
	timeTable = {
		'1':{'1':defaultdict(set),'2':defaultdict(set),'3':defaultdict(set),'4':defaultdict(set),'5':defaultdict(set),'6':defaultdict(set),'7':defaultdict(set),'8':defaultdict(set),'9':defaultdict(set),'10':defaultdict(set),'11':defaultdict(set),'12':defaultdict(set),'13':defaultdict(set)},
		'2':{'1':defaultdict(set),'2':defaultdict(set),'3':defaultdict(set),'4':defaultdict(set),'5':defaultdict(set),'6':defaultdict(set),'7':defaultdict(set),'8':defaultdict(set),'9':defaultdict(set),'10':defaultdict(set),'11':defaultdict(set),'12':defaultdict(set),'13':defaultdict(set)},
		'3':{'1':defaultdict(set),'2':defaultdict(set),'3':defaultdict(set),'4':defaultdict(set),'5':defaultdict(set),'6':defaultdict(set),'7':defaultdict(set),'8':defaultdict(set),'9':defaultdict(set),'10':defaultdict(set),'11':defaultdict(set),'12':defaultdict(set),'13':defaultdict(set)},
		'4':{'1':defaultdict(set),'2':defaultdict(set),'3':defaultdict(set),'4':defaultdict(set),'5':defaultdict(set),'6':defaultdict(set),'7':defaultdict(set),'8':defaultdict(set),'9':defaultdict(set),'10':defaultdict(set),'11':defaultdict(set),'12':defaultdict(set),'13':defaultdict(set)},
		'5':{'1':defaultdict(set),'2':defaultdict(set),'3':defaultdict(set),'4':defaultdict(set),'5':defaultdict(set),'6':defaultdict(set),'7':defaultdict(set),'8':defaultdict(set),'9':defaultdict(set),'10':defaultdict(set),'11':defaultdict(set),'12':defaultdict(set),'13':defaultdict(set)},
		'6':{'1':defaultdict(set),'2':defaultdict(set),'3':defaultdict(set),'4':defaultdict(set),'5':defaultdict(set),'6':defaultdict(set),'7':defaultdict(set),'8':defaultdict(set),'9':defaultdict(set),'10':defaultdict(set),'11':defaultdict(set),'12':defaultdict(set),'13':defaultdict(set)},
		'7':{'1':defaultdict(set),'2':defaultdict(set),'3':defaultdict(set),'4':defaultdict(set),'5':defaultdict(set),'6':defaultdict(set),'7':defaultdict(set),'8':defaultdict(set),'9':defaultdict(set),'10':defaultdict(set),'11':defaultdict(set),'12':defaultdict(set),'13':defaultdict(set)}
	}
	
	def add_arguments(self, parser):
		# Positional arguments
		parser.add_argument('genra', type=str)
		parser.add_argument('course', type=str)
		parser.add_argument('school', type=str)

	def handle(self, *args, **options):
		self.genra = json.load(open(options['genra'], 'r'))
		course = json.load(open(options['course'], 'r'))
		school = options['school']
		self.main(course, school)

		self.stdout.write(self.style.SUCCESS('crawl Job Json success!!!'))

	def main(self, jsonFile, school):
		GenraTable = defaultdict(dict)
		CourseOfDeptTable = defaultdict(dict)

		for course in jsonFile:
			self.forGenra(course, GenraTable)
			self.forDept(course, CourseOfDeptTable)
			self.forTime(course)

		self.sortGenra(GenraTable)
		self.Genra.update_one({'school':school},{'$set': {'school':school, 'Genra':GenraTable}}, upsert=True)

		self.CourseOfDept.update_one({'school':school},{'$set': {'school':school, 'CourseOfDept':CourseOfDeptTable}}, upsert=True)
		self.CourseOfDept.create_index([("school", pymongo.ASCENDING)])

		self.set2tuple()
		self.CourseOfTime.update_one({'school':school}, {'$set':{'school':school, 'CourseOfTime':self.timeTable}}, upsert=True)

	def forGenra(self, course, GenraTable):
		if course['for_dept'] in self.genra:
			GenraTable[self.genra[course['for_dept']]].setdefault(course['for_dept'], set()).add(course['grade'])
		else:
			GenraTable['大學部'].setdefault(course['for_dept'], set()).add(course['grade'])

	def forDept(self, course, CourseOfDeptTable):
		if course['obligatory_tf']:
			CourseOfDeptTable[course['for_dept']].setdefault('obligatory', {}).setdefault(course['grade'], []).append(course['code'])
		else:
			CourseOfDeptTable[course['for_dept']].setdefault('optional', {}).setdefault(course['grade'], []).append(course['code'])

	@staticmethod
	def sortGenra(GenraTable):
		sortingOrder = '一二三四五六日ABCDEFGH'
		for g in GenraTable:
			for key, value in GenraTable[g].items():
				GenraTable[g][key] = sorted(list(value), key=lambda x:sortingOrder.index(x[0]))

	def forTime(self, course):
		for i in course['time']:
			day = i['day']
			for time in i['time']:
				if course['for_dept'] in self.genra:
					self.timeTable[str(day)][str(time)][self.genra[course['for_dept']]].add(course['code'])
				else:
					self.timeTable[str(day)][str(time)][course['for_dept']].add(course['code'])

	def set2tuple(self):
		for day in self.timeTable:
			for time in self.timeTable[day]:
				for codeList in self.timeTable[day][time]:
					self.timeTable[day][time][codeList] = tuple(self.timeTable[day][time][codeList])