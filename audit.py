import csv

scoutmasters = []
scouts = {}
cub_advancement_types = ['Adventure', 'Adventure Requirement','Academics & Sports Belt Loop']

cub_advancement = ['Bobcat','Lion','Tiger','Wolf','Bear','Webelos','Arrow of Light', 'Cub Scout', 'National Summertime Pack Award', 'Shooting Sports','Whittling Chip','Gold Arrow Point','Silver Arrow Point','Outdoor Ethics Awareness Award (Cub Scout)','Outdoor Ethics Action Award (Cub Scout)','Cyber Chip Award (Grades 1-3)','Cyber Chip Award (Grades 4-5)','Paul Bunyan Woodsman','Emergency Preparedness BSA','Religious emblem','Recruiter Strip','Messengers of Peace','International Spirit Award']

for a in ['Adventure', 'Adventure Requirement', 'Rank Requirement', 'Activity Badge', 'Achievement', 'Achievement Requirement','Elective Requirement']:
    for x in ['Bobcat','Lion','Tiger','Wolf','Bear','Webelos','Arrow of Light']:
        cub_advancement_types.append(x + ' ' + a)


with open('roster.csv', newline='') as csvfile:
    roster_reader = csv.reader(csvfile)
    am = True
    ym = False
    for row in roster_reader:
      if len(row) < 2:
          continue
      if(row[1] == 'YOUTH MEMBERS'):
          am = False
          ym = True
      if am and len(row) >=4 and (row[4].find('Scoutmaster') != -1 or row[4].find('Advancement') != -1):
        scoutmasters.append(row[1] + ' ' + row[2])
      if ym and len(row) >= 3:
         if row[1] == 'First Name':
              continue
         #print(row[1] + ' ' + row[2])
         parent_name_index = 5
         parents=[]
         while parent_name_index < len(row):
           if row[parent_name_index] != '':
             parents.append(row[parent_name_index])
           parent_name_index = parent_name_index + 6
         scout = {}
         scout['name'] = row[1] + ' ' + row[2]
         scout['approvers'] = [x for x in scoutmasters if x not in parents]
         scouts[scout['name']]=scout
    
with open('advancement.csv', newline='') as csvfile:
  advancement_reader = csv.reader(csvfile)
  for row in advancement_reader:
      name = row[1] + ' ' + row[3]
      if name =='First Name Last Name':
          continue
      scout = scouts.get(name)
      if scout is None:
          print('skipping unknown scout: ' + name)
          continue

      if row[12] == 'BSA Administrator' or row[12] == '' or row[12] in scout['approvers']:
          continue

      if row[4].strip() in cub_advancement_types or row[5] in cub_advancement:
        continue
      found = False
      for a in cub_advancement:
          if row[5].strip().startswith(a):
              found = True
              break
      if found:
          continue
      if row[5][0].isdigit():
          print(name + '\t--> ' + row[4] + ' ' + row[5] + ' approved by: ' + row[12] + ' on ' + row[13])
      else:
          print(name + '\t--> ' + row[5] + ' approved by: ' + row[12] + ' on ' + row[13])
      

