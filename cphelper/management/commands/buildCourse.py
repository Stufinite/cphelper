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
	
	def add_arguments(self, parser):
		# Positional arguments
		parser.add_argument('genra', type=str)
		parser.add_argument('course', type=str)
		parser.add_argument('school', type=str)

	def handle(self, *args, **options):
		self.genra = json.load(open(options['genra'], 'r'))
		course = json.load(open(options['course'], 'r'))
		school = options['school']
		self.BuildDeptTable(course, school)

		self.stdout.write(self.style.SUCCESS('crawl Job Json success!!!'))

	def BuildDeptTable(self, jsonFile, school):
		GenraTable = defaultdict(dict)
		CourseOfDeptTable = defaultdict(dict)

		for course in jsonFile:
			if course['for_dept'] in self.genra['通識類']:
				GenraTable['通識類'].setdefault(course['for_dept'], set()).add(course['grade'])
			elif course['for_dept'] in self.genra['體育類']:
				GenraTable['體育類'].setdefault(course['for_dept'], set()).add(course['grade'])
			elif course['for_dept'] in self.genra['其他類']:
				GenraTable['其他類'].setdefault(course['for_dept'], set()).add(course['grade'])
			else:
				GenraTable['大學部'].setdefault(course['for_dept'], set()).add(course['grade'])

			if course['obligatory_tf']:
				CourseOfDeptTable[course['for_dept']].setdefault('obligatory', {}).setdefault(course['grade'], []).append(course['code'])
			else:
				CourseOfDeptTable[course['for_dept']].setdefault('optional', {}).setdefault(course['grade'], []).append(course['code'])

		sortingOrder = '一二三四五六日ABCDEFGH'
		for g in GenraTable:
			for key, value in GenraTable[g].items():
				GenraTable[g][key] = sorted(list(value), key=lambda x:sortingOrder.index(x[0]))
		self.Genra.update_one({'school':school},{'$set': {'school':school, 'Genra':GenraTable}}, upsert=True)
		self.CourseOfDept.update_one({'school':school},{'$set': {'school':school, 'CourseOfDept':CourseOfDeptTable}}, upsert=True)

	def BuildByDept(self, jsonDict):
		def getObliAttr(obligat):
			if obligat:
				return 'obligatory'
			return 'optional'

		for i in jsonDict:

			result.setdefault(dept, 
				{
					'obligatory':{},
					'optional':{}
				}
			)

			result[dept][oblAttr].setdefault(grade, []).append(code)

		self.CourseOfDept.remove({})
		
		self.CourseOfDept.insert(resultList)
		self.CourseOfTime.create_index([("school", pymongo.ASCENDING),("dept", pymongo.ASCENDING)])

	def BuildByTime(self, jsonDict):
		result = {
			1:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}},
			2:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}},
			3:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}},
			4:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}},
			5:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}},
			6:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}},
			7:{1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{},11:{},12:{},13:{}}
		}