import random,string, copy, datetime


first_names=["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Mary", "Patricia", "Jenniffer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Nancy"]
last_names=["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

areas=["New Delhi", "Mumbai", "Chennai", "Coimbatore", "Noida", "Kukatpally", "Gurgaon", "Tirpur", "Bellandur","Thane"]
pin=[110001,400001,600001,641001,201301,500072,122001,641601,560103,400601]

no_ppl=100

persons=[]

qualification=["MBBS","MD","BS","MS","Diploma","Metric"]


for i in range(no_ppl):
	ar=random.randrange(len(areas))
	fname=random.randrange(len(first_names))
	if fname<len(first_names)/2:
		gender='M'
	else:
		gender='F'
	number=''.join(["{}".format(random.randint(0, 9)) for num in range(0, 10)])
	uname_length=random.randrange(1,31)
	uname=''.join([random.choice(list(string.ascii_letters)+['_','0','1','2','3','4','5','6','7','8','9']) for i in range(uname_length)])

	pswd_length=random.randrange(1,31)
	pswd=''.join([random.choice(list(string.ascii_letters)+['_','0','1','2','3','4','5','6','7','8','9']) for i in range(pswd_length)])
	persons.append((i+1,first_names[fname],random.choice(last_names),areas[ar],pin[ar],number,gender,random.randrange(101),uname,pswd,uname+"@bla.com",random.choice(qualification)))
	# print(persons[-1])


speciality_list=["Endocrinologist", "Chiropractor", "Psychiatrist", "Bariatric" ,"General Physician", "Pulmonologist", "Ophthalmologist", "Orthopaedic", "ENT", "Dermatologist"]

spec_doc={}

doc_qualification=["MD","MBBS"]

no_docs=2+len(speciality_list)

ppl_copy=copy.deepcopy(persons)

random.shuffle(ppl_copy)

docs=[]

docs_found=0
doc_list=[]

persons_seen=0

spec_added=0

while True:
	if ppl_copy[persons_seen][-1] not in doc_qualification:
		persons_seen+=1
		continue
	docs.append((ppl_copy[persons_seen][0],speciality_list[spec_added],random.randrange(5,10)*1000000,random.choices(['y','n'],weights=[5,1])[0], random.randrange(20), random.randrange(8,21)*50, random.randrange(3,10)*10000))
	spec_doc[speciality_list[spec_added]]=[spec_added]
	persons_seen+=1
	spec_added+=1
	# print(docs[-1])
	if spec_added==len(speciality_list):
		break

for pers in ppl_copy[persons_seen:]:
	if pers[-1] not in doc_qualification:
		continue
	else:
		doc_list.append(pers)
		spec=random.choice(speciality_list)
		if spec not in spec_doc:
			spec_doc[spec]=[]
		spec_doc[spec].append(docs_found)
		docs.append((pers[0], spec, random.randrange(5,10)*1000000,random.choices(['y','n'],weights=[5,1])[0], random.randrange(20), random.randrange(8,21)*50, random.randrange(3,10)*10000))
		# print(docs[-1])
		docs_found+=1
		if docs_found==no_docs-len(speciality_list):
			break

# doc_list=random.sample(persons,k=no_docs)

# docs=[]

# for doc in doc_list:
# 	spec=random.choice(speciality_list)
# 	spec_doc[spec]=doc[0]
# 	docs.append((doc[0],spec,random.choice(qualification),random.randrange(5,10)*1000000,random.choices(['y','n'],weights=[5,1])[0],random.randrange(20),random.randrange(8,21)*50,random.randrange(3,10)*10000))
	# print(docs[-1])


no_support=10

support_list=random.sample(list(set(persons)-set(doc_list)),k=no_support)

# support_qual=["BS","Diploma","Metric"]

support_role=["Technician","Cleaning","Dressing","Reception","Nurse"]

support_staffs=[]

days_of_week=['Mo','Tu','We','Th','Fr','Sa','Su']

for supp in support_list:
	start_hr=random.randrange(24)
	shift_dur=random.randrange(8,15)
	end_hr=(start_hr+shift_dur)%24
	num_days=random.randrange(4,8)
	off_days=random.sample(days_of_week,k=7-num_days)
	working=[x for x in days_of_week if x not in off_days]
	dow=''.join(working)
	support_staffs.append((supp[0],random.choice(support_role),random.randrange(10),random.randrange(5,10)*1000,start_hr,end_hr,dow))
	# print(support_staffs[-1])

no_admin=2

admin_list=random.sample(list(set(persons)),k=no_admin)

# admin_qual=["BS","MS","Diploma"]
admin_role=["Director","Supervisor","IT Head"]

admins=[]

for ad in admin_list:
	# admins.append((ad[0],random.randrange(2,11)*1000000,random.choice(admin_role)))
	admins.append((ad[0],random.randrange(2,11)*1000000))
	# print(admins[-1])



no_patients=500

patients=[]

for i in range(no_patients):
	patients.append((random.choice(persons)[0],i+1))


# generate 4 weeks of data
no_weeks=4
start_date = datetime.datetime.strptime("01-02-2021", "%d-%m-%Y")
end=start_date+datetime.timedelta(weeks=no_weeks)
# end = datetime.datetime.strptime("01-03-2021", "%d-%m-%Y")
date_generated = [start_date + datetime.timedelta(days=x) for x in range(0, (end-start_date).days)]

# for date in date_generated:
#     print(date.strftime("%d-%m-%Y"))

start_time=datetime.datetime.strptime("00:00","%H:%M")
time_generated=[start_time+datetime.timedelta(minutes=i*30) for i in range(48)]

# for t in time_generated:
# 	print(t.strftime("%H:%M"))

slots=[]

for d in date_generated:
	for t in time_generated:
		slots.append((d.strftime("%d-%m-%Y"),t.strftime("%H:%M")))


no_rooms=20

rooms=[]
beds=[]

bed_room=[]

rooms_alotted=0
beds_allotted=0

for i in range(int(no_rooms*0.6)):
	rooms.append((rooms_alotted+1,"Examination"))
	beds.append((beds_allotted,"Examination",0))
	bed_room.append((beds_allotted+1,rooms_alotted+1))
	rooms_alotted+=1
	beds_allotted+=1

# print(rooms)

for i in range(int(no_rooms*0.15)):
	rooms.append((rooms_alotted+1,"OT"))
	beds.append((beds_allotted+1,"OT",0))
	bed_room.append((beds_allotted+1,rooms_alotted+1))
	rooms_alotted+=1
	beds_allotted+=1

for i in range(int(no_rooms*0.20)):
	rooms.append((rooms_alotted+1,"Ward"))
	for j in range(8):
		beds.append((beds_allotted+1,"Type1",1000))
		bed_room.append((beds_allotted+1,rooms_alotted+1))
		# print(beds[-1])
		beds_allotted+=1
	for j in range(2):
		beds.append((beds_allotted+1,"Type1s",1500))
		bed_room.append((beds_allotted+1,rooms_alotted+1))
		# print(beds[-1])
		beds_allotted+=1
	rooms_alotted+=1

for i in range(int(no_rooms*0.05)):
	rooms.append((rooms_alotted+1,"Spl Ward"))
	for j in range(4):
		beds.append((beds_allotted+1,"Type2",2000))
		bed_room.append((beds_allotted+1,rooms_alotted+1))
		# print(beds[-1])
		beds_allotted+=1
	for j in range(1):
		beds.append((beds_allotted+1,"Type2s",2500))
		bed_room.append((beds_allotted+1,rooms_alotted+1))
		# print(beds[-1])
		beds_allotted+=1
	rooms_alotted+=1



disease_list=["Hypertension", "Diabetes", "Back pain", "Anxiety", "Obesity", "Allergy", "Esophagitis", "Asthma", "Visual refractive errors", "Osteoarthritis", "Joint pain", "Sinusitis", "Depression", "Bronchitis", "Fungal infection"]
disease_link=["https://www.medicalnewstoday.com/articles/150109", "https://www.medicalnewstoday.com/articles/323627", "https://www.medicalnewstoday.com/articles/172943",
"https://www.medicalnewstoday.com/articles/323454", "https://www.medicalnewstoday.com/articles/323551", "https://www.healthline.com/health/allergies", "https://www.healthline.com/health/esophagitis",
"https://www.medicalnewstoday.com/articles/323523","https://en.wikipedia.org/wiki/Refractive_error","https://www.mayoclinic.org/diseases-conditions/osteoarthritis/diagnosis-treatment/drc-20351930",
"https://www.healthline.com/health/joint-pain","https://www.medicalnewstoday.com/articles/149941", "https://www.healthline.com/health/depression", "https://www.medicalnewstoday.com/articles/8888","https://www.medicalnewstoday.com/articles/317970"]
dis_speciality=[0,0,1,2,3,4,5,5,6,7,7,8,2,5,9]


diseases=[]

for i in range(len(disease_list)):
	diseases.append((i+1,disease_list[i],disease_link[i]))


tests=[]

tests.append((1,"Blood test",200))
tests.append((2,"MRI",6000))
tests.append((3,"X-Ray",500))
tests.append((4,"RTPCR",2000))
tests.append((5,"CT",5000))

equipment_list=["MRI","X-Ray","RTPCR","CT"]
no_each_equip=2
eq_no=0
equipments=[]

for (j,e) in enumerate(equipment_list):
	for i in range(no_each_equip):
		equipments.append((eq_no+1,e+str(i+1),random.randrange(1,no_rooms+1),j+2))
		# print(equipments[-1])
		eq_no+=1

handles=[]
assg_tos=[]

eq_assinged=0

for supp in support_staffs:
	if random.choice([True,False]) and eq_assinged<len(equipments):# assign an equipment
		handles.append((supp[0],eq_assinged+1))
		# print("H:",handles[-1])
		eq_assinged+=1
	else:
		assg_tos.append((supp[0],random.randrange(1,no_rooms+1)))
		# print(assg_tos[-1])





dis_symp=[[0,1,2,3],[4,5,6,7,12],[8],[12,9,10,11],[13],[14,15,16,19],[17,18,2],[19,3,10],[0,7],[20,21],[20],[15,0,22],[23],[22,1,3,2],[16,24]]
symptom_list=["Headache","Fatigue","Chest Pain","Breathing difficulty","Very thirsty","Very hungry","Unexplained weight loss","Blurry vision","Back pain","Nervousness","Increased heart rate","Panic","Tiredness",
"High BMI","Sneezing","Blocked nose","Itch","Difficulty swallowing","Heartburn","Wheezing","Joint pain","Joint stiffness","Cough","Sad","Skin redness"]

symptoms=[]

for (i,s) in enumerate(symptom_list):
	symptoms.append((i+1,s))

doc_free_slots={}

doc_room=random.sample(list(range(int(no_rooms*0.6))),k=no_docs)

doc_room_slots=[]
no_drs_entries=0

# print(docs,"\n\n\n")

no_slots=50

for (i,doc) in enumerate(docs):
	# print(doc)
	slots_chosen=random.sample(list(range(7*48)),k=no_slots)
	doc_free_slots[doc[0]]=[]
	for j in range(no_weeks): #no of weeks
		# print("bla")
		for k in slots_chosen:
			doc_room_slots.append((doc[0],doc_room[i],slots[j*7*48+k][0],slots[j*7*48+k][1]))
			doc_free_slots[doc[0]].append(no_drs_entries)
			# print(doc_room_slots[-1])
			no_drs_entries+=1
			
# print(doc_free_slots)


medicine_list=["Aspirin","Vitamin C", "Riboflavin", "Tetracycline","Captoporil","Chloroquine","Dexamaethasone","Diosmin","Salbutamol","Erythromycin"]
med_manufacturer=["Zydus","Neo","Nostrum","Pharm","Kydus","Apropos","Zydus","Apropos","Nostrum","Das"]
med_price=[10,50,30,100,200,150,300,32,200,15]

medicines=[]
for i in range(len(medicine_list)):
	medicines.append((i+1,medicine_list[i],"dawa",med_manufacturer[i],med_price[i]))


suffers=[]
meets=[]
appointments=[]
prescriptions=[]
medss=[]
should_takes=[]

shows=[]

bills=[]

no_app=0

med_freq=["OD","TD","W","Need"]

payment_choices=["Cash","Cheque","Card","Online"]


def add_prescription(presc_no):
	prescriptions.append((presc_no,""))
	no_meds=random.randrange(5)
	no_tests=random.randrange(3)
	meds=random.sample(medicines, k=no_meds)
	ts=random.sample(tests,k=no_tests)

	for med in meds:
		medss.append((med[0],presc_no,"",random.choice(med_freq)))
		# print("Meds: ",medss[-1])
	for t in ts:
		should_takes.append((presc_no,t[0]))
		# print("Tests: ",should_takes[-1])

def add_app_bill(app_no):
	paid=random.choices([None,pat[0]],weights=[0.2,0.8])[0]
	mode=None
	if paid is not None:
		mode=random.choice(payment_choices)
	bills.append((no_app,None,"OPD",random.randrange(3)*10,mode))
	# print(bills[-1])

def add_symps(disease,app_id):
	poss_symp=dis_symp[disease[0]-1]
	no_symp=len(poss_symp)
	shown_symp=random.randrange(1,no_symp+1)
	symps=random.sample(poss_symp,k=shown_symp)

	for symp in symps:
		shows.append((app_id,symp+1))
		# print(shows[-1])

for pat in patients[:int(len(patients)*0.8)]:


	# print("Patient:", pat)

	# assign a disease
	disease=random.choice(diseases)
	if random.choices([True,False],weights=[0.9,0.1])[0]: # diagnosed yet or not
		suffers.append((pat[1],disease[0]))
		# print("Suffers: ",suffers[-1])
	# else:
		# print("Not diagnosed for ",disease)

	no_meets=random.choice([1,2,3])

	# for first meet, could meet with gp or specialist
	doc_spl=random.choices([4,dis_speciality[disease[0]-1]],weights=[0.2,0.8])[0]
	doc=random.choice(spec_doc[speciality_list[doc_spl]])
	doc=docs[doc]

	# print(doc)
	# print(doc_free_slots[doc[0]])
	last_meet=doc_free_slots[doc[0]][0]

	doc_free_slots[doc[0]].remove(last_meet)


	no_app+=1
	drs_entry=doc_room_slots[last_meet]

	meets.append((no_app,pat[1],doc[0],drs_entry[2],drs_entry[3],""))
	# print(meets[-1])

	add_symps(disease,no_app)



	add_app_bill(no_app)
	appointments.append((no_app,"OPD",no_app,no_app))
	# print(appointments[-1])
	add_prescription(no_app)

	for i in range(1,no_meets):
		doc_spl=dis_speciality[disease[0]-1]
		doc=random.choice(spec_doc[speciality_list[doc_spl]])
		doc=docs[doc]

		# print(doc)
		# print(doc_free_slots[doc[0]])
		last_meet=doc_free_slots[doc[0]][0] # enforce that this meeting is only after the previous one?

		doc_free_slots[doc[0]].remove(last_meet)

		no_app+=1
		drs_entry=doc_room_slots[last_meet]
		meets.append((no_app,pat[1],doc[0],drs_entry[2],drs_entry[3],""))
		# print(meets[-1])

		add_symps(disease,no_app)

		add_app_bill(no_app)
		appointments.append((no_app,"OPD",no_app,no_app))
		# print(appointments[-1])
		add_prescription(no_app)

	# if no_app>=20:
	# 	break



	# prescription, medicine, bill, tests, ...
	# prescriptions.append((no_app,))


bills_generated=no_app
occupiess=[]
visitss=[]

beds_assigned=0
total_beds=int(no_rooms*2.25)

days_group=int(no_weeks*7*total_beds/(len(patients)*0.2))-1
# print("DG:",days_group)

assert(days_group>2)

days_group_travelled=0

for pat in patients[int(len(patients)*0.8):]:
	no_days=random.randrange(1,days_group)

	start_offset=random.randrange(no_days)

	occ_start=start_date+datetime.timedelta(days=days_group_travelled*days_group+start_offset)
	occ_end=start_date+datetime.timedelta(days=days_group_travelled*days_group+no_days)
	bills_generated+=1
	occupiess.append((pat[1],beds_assigned+1+int(0.75*no_rooms),occ_start.strftime("%d-%m-%Y"),occ_end.strftime("%d-%m-%Y"),bills_generated))

	# print("Occ: ",occupiess[-1])

	paid=random.choices([True,False],weights=[0.8,0.2])[0]
	if paid:
		bills.append((bills_generated,None,"Admission",random.randrange(3)*10,random.choice(payment_choices)))
	else:
		bills.append((bills_generated,None,"Admission",random.randrange(3)*10,None))

	# print("Bill: ",bills[-1])

	beds_assigned+=1
	if beds_assigned==total_beds:
		days_group_travelled+=1
		beds_assigned=0

	

	if random.choices([True,False],weights=[0.4,0.6])[0]:# if the doctor visits
		visitss.append((pat[1],random.choice(docs)[0],occ_start.strftime("%d-%m-%Y"),""))
		# print("Vis:",visitss[-1])


no_tests_taken=100
takess=[]

for i in range(no_tests_taken):
	dat=start_date+datetime.timedelta(days=random.randrange(no_weeks*7))
	bills_generated+=1
	takess.append((random.choice(patients)[1],random.choice(tests)[0],random.choice(["NULL","results/test"+str(i)+".pdf"]),"",dat.strftime("%d-%m-%Y"),bills_generated))
	# print(takess[-1])
	paid=random.choices([True,False],weights=[0.8,0.2])[0]
	if paid:
		bills.append((bills_generated,None,"Diagnosis",random.randrange(3)*10,random.choice(payment_choices)))
	else:
		bills.append((bills_generated,None,"Diagnosis",random.randrange(3)*10,None))
	# print(bills[-1])



# random pharmacy purchases

bill_meds=[]

no_outside_purchases=50
for i in range(no_outside_purchases):
	bills_generated+=1
	bills.append((bills_generated,random.choice(persons)[0],"Pharmacy",0,random.choice(payment_choices)))
	# print(bills[-1])
	no_meds_purchased=random.randrange(1,len(medicines)+1)
	med_purchased=random.sample(medicines,k=no_meds_purchased)
	for med in med_purchased:
		bill_meds.append((bills_generated,med[0],random.randrange(1,10)))
		# print(bill_meds[-1])

	# print("\n\n")
	

# history
historys=[]

smallest_date=datetime.datetime.strptime("01-02-2019", "%d-%m-%Y")
for pat in patients:
	if random.choice([True,False]):
		no_hist=random.randrange(1,len(disease_list))
		for i in range(no_hist):
			date=smallest_date+datetime.timedelta(days=random.randrange(500))
			historys.append((pat[0],random.choice(diseases)[0],random.choice(["Self","Relative"]),date.strftime("%d-%m-%Y")))
			# print(historys[-1])








