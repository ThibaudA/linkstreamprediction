import sys
import numpy as np
from metrics import metrics
from evaluation import evaluate
from scoring import score
from math import floor
import itertools
import matplotlib.pyplot as plt
import operator
from operator import itemgetter, attrgetter
import os
# nodes = dict() # observation
times = dict() # observation
predtimes=dict()
N=1000. #nb of point for small plot function
metrics= metrics()
freq=0
linkbyarea=0

if len(sys.argv)!=2:
	sys.stderr.write("0  #start time of TrainingObservation \n")
	sys.stderr.write("100 #end time of TrainingObservation\n")

	sys.stderr.write("50 #start time of TrainingPrediction\n")
	sys.stderr.write("100 #end time of TrainingPrediction\n")

	sys.stderr.write("0  #start time of Observation \n")
	sys.stderr.write("100 #end time of Observation\n")

	sys.stderr.write("50 #start time of Prediction\n")
	sys.stderr.write("100 #end time of Prediction\n")

	sys.stderr.write("Metrics #Metrics used\n")
	sys.stderr.write("intercontactTimes\n")
	sys.stderr.write("commonNeighbors\n\n")

	sys.stderr.write("Opp\n")
	sys.stderr.write("+ #operator used\n \n")

	sys.stderr.write("Commentaries:\n")

	sys.stderr.write("Bla bla \n")
	exit(1)
else:
	conf = open(sys.argv[1], 'r')
	tstartobsT = float(conf.readline().split("#")[0].strip(" "))  #start time of Trainingobservation
	tendobsT=float(conf.readline().split("#")[0].strip(" ")) #end time of Trainingobservation
	tstartpredT =  float(conf.readline().split("#")[0].strip(" "))  #start time of training Pred
	tendpredT = float(conf.readline().split("#")[0].strip(" "))  #end time of training Pred
	T = tendpredT - tstartpredT #trainingpred duration (temporaire)

	tstartobs = float(conf.readline().split("#")[0].strip(" "))  #start time of observation
	tendobs=float(conf.readline().split("#")[0].strip(" ")) #end time of observation
	tstartpred =  float(conf.readline().split("#")[0].strip(" ")) 	#start time of Pred
	tendpred = float(conf.readline().split("#")[0].strip(" "))  #end time of Pred

	sc=score()

	MetricsOK = False
	sys.stderr.write(conf.readline().split("#")[0].strip(" ") + ":\n")
	while MetricsOK != True:
		line = conf.readline()
		if line != "Opperator used:\n":
			if len(line.split(" "))!=1: # if one or more parameter
				metrics._confmetrics[line.split(" ")[0]]=list(map(float,line.rstrip("\n").split(" ")[1].split(",")))
			else:
				metrics._confmetrics[line.split(" ")[0].rstrip("\n")]=[1.]
		else:
			MetricsOK=True
sys.stderr.write(str(metrics._confmetrics)+"\n")
sc._opperator= conf.readline().split(" ")[0].rstrip("\n")
line = conf.readline().split(" ")
if line[0].rstrip("\n") == "Extract":
	ExtractDirectory=line[1].rstrip("\n")
	Extract = True
	print(ExtractDirectory)
	dir = os.path.dirname(ExtractDirectory+"/")
	try:
	    os.stat(dir)
	except:
	    os.mkdir(dir)

sys.stdout.write("Operator: "+str(sc._opperator)+"\n")
# print "t=",t,"\ntmesure=", tmesure,"\nT=",T,"\nn=",n

sys.stdout.write("tstartobsT: "+str(tstartobsT)+"\n")
sys.stdout.write("tendobsT: "+str(tendobsT)+"\n")
sys.stdout.write("tstartpredT: "+str(tstartpredT)+"\n")
sys.stdout.write("tsendpredT: "+str(tendpredT)+"\n")

sys.stdout.write("tstartobs: "+str(tstartobs)+"\n")
sys.stdout.write("tendobs: "+str(tendobs)+"\n")
sys.stdout.write("tstartpred: "+str(tstartpred)+"\n")
sys.stdout.write("tsendpred: "+str(tendpred)+"\n")


t= 0
nb_linksPRED=0

while t<tstartobsT:
	line = sys.stdin.readline()
	contents = line.split(" ")
	t = float(contents[0])

sys.stderr.write("Starting mesure at: "+str(t)+"\n")
while t<tendpred:
	line = sys.stdin.readline()
	contents = line.split(" ")
	t = float(contents[0])
	if (tstartobsT<=t<tendobsT) or (tstartpredT<=t<tendpredT) or (tstartobs<=t<tendobs):
		u = int(contents[1])
		v = int(contents[2])
		link= frozenset([u,v])
		if not link in times:
			times[link] = []
		#sc.addPair(link)
		times[link].append(t)

	if tstartpred<=t<tendpred:
		u = int(contents[1])
		v = int(contents[2])
		link= frozenset([u,v])
		if not link in predtimes:
			predtimes[link] = []
		predtimes[link].append(t)

		nb_linksPRED=nb_linksPRED + 1

for line in sys.stdin.read(): #to avoid cat error message
	a=1


nb_linksOBS=0
nb_linksOBS1=0
nb_linksOBS2=0

nb_linksTRAINING=0
obstimes=dict()
trainingtimes=dict()
for link in times:
	obstimes[link]=[x for x in times[link] if x>=tstartobsT and x<tendobsT]
	if len(obstimes[link])==0:
		del obstimes[link]
	trainingtimes[link]=[x for x in times[link] if x>=tstartpredT and x<tendpredT]
	if len(trainingtimes[link])==0:
		del trainingtimes[link]

obsnodes=dict()
for link in obstimes:
	u,v = link
	if u not in obsnodes:
		obsnodes[u]=set()
	if v not in obsnodes:
		obsnodes[v]=set()
	obsnodes[u].add(v)
	# print(obsnodes[v])
	obsnodes[v].add(u)
	# print(obsnodes[v])
	nb_linksOBS1 = nb_linksOBS1 + len([x for x in obstimes[link] if x>=tstartobsT and x<(tendobsT+tstartobsT)/2])
	nb_linksOBS2 = nb_linksOBS2 + len([x for x in obstimes[link] if x>=(tendobsT+tstartobsT)/2 and x<tendobsT])
	nb_linksOBS=nb_linksOBS1+nb_linksOBS2

if Extract:
	score.extractTime(obstimes,ExtractDirectory+ "/ExtractOBS")
	score.extractTime(trainingtimes,ExtractDirectory+ "/ExtractTRAIN")



trainingtimesaggregated=dict()
for link in trainingtimes:
	nb_linksTRAINING = nb_linksTRAINING + len(trainingtimes[link])
	trainingtimesaggregated[link]= len(trainingtimes[link])

sys.stdout.write("TRAINING:\n")

sys.stdout.write("Nblinks OBS "+str(nb_linksOBS)+"\n")
sys.stdout.write("Nblinks TRAINING C0 "+str(nb_linksTRAINING)+"\n")

#Class Making
#3 Class : C1 = New link C2 = less than 5 link C3 more than 5
# sc.traceActivityhistogram(50,obstimes)
sc1=score()
sc2=score()
sc3=score()
scPLUS=score()

classthreshold = 5
for u,v in itertools.combinations(obsnodes.keys(),2): #to predict new pair of nodes
	link = frozenset([u,v])
	sc.addPair(link)
	scPLUS.addPair(link)
	if link not in obstimes:
		sc1.addPair(link)
	elif len(obstimes[link]) < classthreshold:
		sc2.addPair(link)
	else:
		sc3.addPair(link)


nb_linksTRAININGC1,nb_linksTRAININGC2,nb_linksTRAININGC3=0,0,0
for link in trainingtimes:
	if link in sc1._pair_set:
		nb_linksTRAININGC1 += len(trainingtimes[link])
	elif link in sc2._pair_set:
		nb_linksTRAININGC2 += len(trainingtimes[link])
	elif link in sc3._pair_set:
		nb_linksTRAININGC3 += len(trainingtimes[link])

sys.stdout.write("Nblinks TRAINING C1 "+str(nb_linksTRAININGC1)+"\n")
sys.stdout.write("Nblinks TRAINING C2 "+str(nb_linksTRAININGC2)+"\n")
sys.stdout.write("Nblinks TRAINING C3 "+str(nb_linksTRAININGC3)+"\n")

#ALL
metrics.computeMetrics(sc,tstartobsT,tendobsT,obstimes,obsnodes) #compute all metrics
sc.integrateMetrics(tstartpredT,tendpredT) #integrate metrics
# sc.correlationMatrix(metrics._confmetrics)
# sys.exit()
sc.setMaxByMetric()
sc.normalizeMetrics()
if Extract:
	sc.extractMetric(metrics._confmetrics,ExtractDirectory+ "/ExtractMetrics")
#C1
metrics.computeMetrics(sc1,tstartobsT,tendobsT,obstimes,obsnodes) #compute all metrics
sc1.integrateMetrics(tstartpredT,tendpredT) #integrate metrics
sc1.setMaxByMetric()
sc1.normalizeMetrics()
#C2
metrics.computeMetrics(sc2,tstartobsT,tendobsT,obstimes,obsnodes) #compute all metrics
sc2.integrateMetrics(tstartpredT,tendpredT) #integrate metrics
sc2.setMaxByMetric()
sc2.normalizeMetrics()
#C3
metrics.computeMetrics(sc3,tstartobsT,tendobsT,obstimes,obsnodes) #compute all metrics
sc3.integrateMetrics(tstartpredT,tendpredT) #integrate metrics
sc3.setMaxByMetric()
sc3.normalizeMetrics()
#PLUS
metrics.computeMetrics(scPLUS,tstartobsT,tendobsT,obstimes,obsnodes) #compute all metrics
scPLUS.integrateMetrics(tstartpredT,tendpredT) #integrate metrics
scPLUS.setMaxByMetric()
scPLUS.normalizeMetrics()

#extrapolate the activity as constant
# n=metrics.linearActivityExtrapolation(nb_linksOBS,tstartobsT,tendobsT,tstartpredT,tendpredT)
#n=metrics.fitnPointrActivityExtrapolation(obstimes,tstart,tendobs,tmesure,tendtraining,30)
# n=metrics.twopointrActivityExtrapolation(nb_linksOBS1,nb_linksOBS2,tstart,(tstart+tendobs)/2,tendobs,tmesure,tendtraining)
#Triche
n= nb_linksTRAINING
sys.stdout.write("Nblinks predicted C0 "+str(n)+"\n")
# #Determine the ratio between the classes
# n1=0
# n2=0
# n3=0
# for link in trainingtimes:
# 	if link in sc1._pair:
# 		n1=n1+len(trainingtimes[link])
# 	if link in sc2._pair:
# 		n2=n2+len(trainingtimes[link])
# 	if link in sc3._pair:
# 		n3=n3+len(trainingtimes[link])
#
# ratio1= n1/n
# ratio2= n2/n
# ratio3= n3/n
# sys.stdout.write("Nblinks predicted C1 "+str(n1)+"\n")
# sys.stdout.write("Nblinks predicted C2 "+str(n2)+"\n")
# sys.stdout.write("Nblinks predicted C3 "+str(n3)+"\n")

# sc.OnePred(tstartobsT,tendobsT,tstartpredT,tendpredT,n,obstimes,trainingtimesaggregated,metrics._confmetrics)

# initconfmetrics = sc.gridsearch(tstartobsT,tendobsT,tstartpredT,tendpredT,n,trainingtimesaggregated,metrics._confmetrics)
# initconfmetrics1 = sc1.gridsearch(tstartobsT,tendobsT,tstartpredT,tendpredT,n1,trainingtimesaggregated,metrics._confmetrics)
# initconfmetrics2 = sc2.gridsearch(tstartobsT,tendobsT,tstartpredT,tendpredT,n2,trainingtimesaggregated,metrics._confmetrics)
# initconfmetrics3 = sc3.gridsearch(tstartobsT,tendobsT,tstartpredT,tendpredT,n3,trainingtimesaggregated,metrics._confmetrics)
initconfmetrics = sc.randomExplo(tstartobsT,tendobsT,tstartpredT,tendpredT,n,trainingtimesaggregated,metrics._confmetrics,10000)
# initconfmetrics1 = sc1.randomExplo(tstartobsT,tendobsT,tstartpredT,tendpredT,n1,trainingtimesaggregated,metrics._confmetrics,4000)
# initconfmetrics2 = sc2.randomExplo(tstartobsT,tendobsT,tstartpredT,tendpredT,n2,trainingtimesaggregated,metrics._confmetrics,4000)
# initconfmetrics3 = sc3.randomExplo(tstartobsT,tendobsT,tstartpredT,tendpredT,n3,trainingtimesaggregated,metrics._confmetrics,4000)
initconfmetrics1,initconfmetrics2,initconfmetrics3 = scPLUS.randomExploPLUS(tstartobsT,tendobsT,tstartpredT,tendpredT,n,trainingtimesaggregated,metrics._confmetrics,15000,sc1,sc2,sc3)
#
# sys.stderr.write("fin train "+str(initconfmetrics)+" \n \n")
# sys.stderr.write("fin train C1 "+str(initconfmetrics1)+" \n \n")
# sys.stderr.write("fin train C2"+str(initconfmetrics2)+" \n \n")
# sys.stderr.write("fin train C3"+str(initconfmetrics3)+" \n \n")
sys.stderr.write("fin init "+str(initconfmetrics)+" \n")
sys.stderr.write("fin init C1 "+str(initconfmetrics1)+" \n")
sys.stderr.write("fin init C2"+str(initconfmetrics2)+" \n")
sys.stderr.write("fin init C3"+str(initconfmetrics3)+" \n")

derstep = 0.05
sizelinexptep = 0.05
numlinexptep = 100
#perform gradient descent to better tune the parameters

predconfmetric, Finalscore =sc.gradDescentLinExp(tstartobsT,tendobsT,tstartpredT,tendpredT,n,trainingtimesaggregated,initconfmetrics,derstep,sizelinexptep,numlinexptep)
sys.stderr.write("C0 Done\n")
# predconfmetric1,Finalscore1=sc1.gradDescentLinExp(tstartobsT,tendobsT,tstartpredT,tendpredT,n1,trainingtimesaggregated,initconfmetrics1,derstep,sizelinexptep,numlinexptep)
# predconfmetric2,Finalscore2=sc2.gradDescentLinExp(tstartobsT,tendobsT,tstartpredT,tendpredT,n2,trainingtimesaggregated,initconfmetrics2,derstep,sizelinexptep,numlinexptep)
# predconfmetric3,Finalscore3=sc3.gradDescentLinExp(tstartobsT,tendobsT,tstartpredT,tendpredT,n3,trainingtimesaggregated,initconfmetrics3,derstep,sizelinexptep,numlinexptep)
predconfmetric1,predconfmetric2,predconfmetric3,FinalscorePLUS,Finalscore1,Finalscore2,Finalscore3=scPLUS.gradDescentLinExpPLUS(tstartobsT,tendobsT,tstartpredT,tendpredT,n,trainingtimesaggregated,initconfmetrics1,initconfmetrics2,initconfmetrics3,derstep,sizelinexptep,numlinexptep,1000,sc1,sc2,sc3)
sys.stderr.write("C123 Done\n")

if Extract:
	score.extractCoef(predconfmetric,predconfmetric1,predconfmetric2,predconfmetric3,ExtractDirectory+ "/ExtractCoefs")
	sc.extractPrediction(ExtractDirectory+ "/ExtractPredC0")
	sc1.extractPrediction(ExtractDirectory+ "/ExtractPredC1")
	sc2.extractPrediction(ExtractDirectory+ "/ExtractPredC2")
	sc3.extractPrediction(ExtractDirectory+ "/ExtractPredC3")




nb_linksPredictedC01,nb_linksPredictedC02,nb_linksPredictedC03=0,0,0
for link in sc._ranks:
	if link in sc1._pair_set:
		nb_linksPredictedC01 += sc._ranks[link]
	elif link in sc2._pair_set:
		nb_linksPredictedC02 += sc._ranks[link]
	elif link in sc3._pair_set:
		nb_linksPredictedC03 += sc._ranks[link]

sys.stdout.write("Nblinks predicted C0 "+str(n)+"\n")
sys.stdout.write("Nblinks predicted C01 "+str(nb_linksPredictedC01)+"\n")
sys.stdout.write("Nblinks predicted C02 "+str(nb_linksPredictedC02)+"\n")
sys.stdout.write("Nblinks predicted C03 "+str(nb_linksPredictedC03)+"\n")


nb_linksPredictedC1,nb_linksPredictedC2,nb_linksPredictedC3=0,0,0
for link in sc._ranks:
	if link in sc1._pair_set:
		nb_linksPredictedC1 += scPLUS._ranks[link]
	elif link in sc2._pair_set:
		nb_linksPredictedC2 += scPLUS._ranks[link]
	elif link in sc3._pair_set:
		nb_linksPredictedC3 += scPLUS._ranks[link]

sys.stdout.write("Nblinks predicted C1 "+str(nb_linksPredictedC1)+"\n")
sys.stdout.write("Nblinks predicted C2 "+str(nb_linksPredictedC2)+"\n")
sys.stdout.write("Nblinks predicted C3 "+str(nb_linksPredictedC3)+"\n")
ev01 = evaluate()
ev02 = evaluate()
ev03 = evaluate()
ev01.calculateScore({x:sc._ranks[x] for x in sc1._ranks},trainingtimes)
ev02.calculateScore({x:sc._ranks[x] for x in sc2._ranks},trainingtimes)
ev03.calculateScore({x:sc._ranks[x] for x in sc3._ranks},trainingtimes)
if Extract:
	evaluate.extractQualitybypair(sc._ranks,trainingtimes,ExtractDirectory+ "/ExtractQualitybypairC0")
	evaluate.extractQualitybypair(sc1._ranks,trainingtimes,ExtractDirectory+ "/ExtractQualitybypairC1")
	evaluate.extractQualitybypair(sc2._ranks,trainingtimes,ExtractDirectory+ "/ExtractQualitybypairC2")
	evaluate.extractQualitybypair(sc3._ranks,trainingtimes,ExtractDirectory+ "/ExtractQualitybypairC3")


sys.stdout.write("C0: \n")
Finalscore.printeval()
sys.stdout.write("C0_1: \n")
ev01.printeval()
sys.stdout.write("C0_2: \n")
ev02.printeval()
sys.stdout.write("C0_3: \n")
ev03.printeval()
sys.stdout.write("CPLUS: \n")
FinalscorePLUS.printeval()
sys.stdout.write("C1: \n")
Finalscore1.printeval()
sys.stdout.write("C2: \n")
Finalscore2.printeval()
sys.stdout.write("C3: \n")
Finalscore3.printeval()


#sys.stderr.write("\nInit " +str(initconfmetrics)+" "+ str(MFscore)+"\n")
sys.stderr.write("fin train "+str(predconfmetric)+" "+str(Finalscore._F)+"\n \n")
sys.stderr.write("fin train C1 "+str(predconfmetric1)+" "+str(Finalscore1._F)+"\n \n")
sys.stderr.write("fin train C2"+str(predconfmetric2)+" "+str(Finalscore2._F)+"\n \n")
sys.stderr.write("fin train C3"+str(predconfmetric3)+" "+str(Finalscore3._F)+"\n \n")

#Fin Training Debut Prediction

nb_linksOBS=0
nb_linksOBS1=0
nb_linksOBS2=0
obstimes=dict()
obsnodes=dict()
for link in times:
	obstimes[link]=[x for x in times[link] if x>=tstartobs and x<tendobs]
	if len(obstimes[link])==0:
		del obstimes[link]

for link in obstimes:
	u,v = link
	if u not in obsnodes:
		obsnodes[u]=set()
	if v not in obsnodes:
		obsnodes[v]=set()
	obsnodes[u].add(v)
	obsnodes[v].add(u)
	nb_linksOBS1 = nb_linksOBS1 + len([x for x in obstimes[link] if x>=tstartobs and x<(tendobs+tstartobs)/2])
	nb_linksOBS2 = nb_linksOBS2 + len([x for x in obstimes[link] if x>=(tendobs+tstartobs)/2 and x<tendobs])
	nb_linksOBS=nb_linksOBS1+nb_linksOBS2



predtimesaggregated=dict()
for link in predtimes:
	predtimesaggregated[link]= len(predtimes[link])


sc.resetPairs() #making sure sc is clear (could have created another but memory)
sc.resetRanks()
sc1.resetPairs() #making sure sc is clear (could have created another but memory)
sc1.resetRanks()
sc2.resetPairs() #making sure sc is clear (could have created another but memory)
sc2.resetRanks()
sc3.resetPairs() #making sure sc is clear (could have created another but memory)
sc3.resetRanks()
scPLUS.resetPairs() #making sure sc is clear (could have created another but memory)
scPLUS.resetRanks()

for u,v in itertools.combinations(obsnodes.keys(),2): #to predict new pair of nodes
	link = frozenset([u,v])
	sc.addPair(link)
	if link not in obstimes:
		sc1.addPair(link)
	elif len(obstimes[link]) < classthreshold:
		sc2.addPair(link)
	else:
		sc3.addPair(link)

metrics.computeMetrics(sc,tstartobs,tendobs,obstimes,obsnodes)
sc.integrateMetrics(tstartpred,tendpred)
sc.setMaxByMetric()
sc.normalizeMetrics()
sc.rankPairs(tstartpred,tendpred,predconfmetric)

metrics.computeMetrics(sc1,tstartobs,tendobs,obstimes,obsnodes)
sc1.integrateMetrics(tstartpred,tendpred)
sc1.setMaxByMetric()
sc1.normalizeMetrics()
sc1.rankPairs(tstartpred,tendpred,predconfmetric1)

metrics.computeMetrics(sc2,tstartobs,tendobs,obstimes,obsnodes)
sc2.integrateMetrics(tstartpred,tendpred)
sc2.setMaxByMetric()
sc2.normalizeMetrics()
sc2.rankPairs(tstartpred,tendpred,predconfmetric2)

metrics.computeMetrics(sc3,tstartobs,tendobs,obstimes,obsnodes)
sc3.integrateMetrics(tstartpred,tendpred)
sc3.setMaxByMetric()
sc3.normalizeMetrics()
sc3.rankPairs(tstartpred,tendpred,predconfmetric3)

metrics.computeMetrics(scPLUS,tstartobsT,tendobsT,obstimes,obsnodes) #compute all metrics
scPLUS.integrateMetrics(tstartpredT,tendpredT) #integrate metrics
scPLUS.setMaxByMetric()
scPLUS.normalizeMetrics()

n=metrics.linearActivityExtrapolation(nb_linksOBS,tstartobs,tendobs,tstartpred,tendpred)
# n=nb_linksPRED
#n=metrics.twopointrActivityExtrapolation(nb_linksOBS1,nb_linksOBS2,tstartobs,(tstartobs+tendobs)/2,tendobs,tstartpred,tendpred)
# n1=ratio1*n
# n2=ratio2*n
# n3=ratio3*n



sc.normalizeranksbyintegral(n)
Mergeranks=sc1._ranks.copy()
Mergeranks.update(sc2._ranks)
Mergeranks.update(sc3._ranks)
scPLUS._ranks=Mergeranks
scPLUS.normalizeranksbyintegral(n)


sys.stdout.write("PREDICTION\n")
sys.stdout.write("Nblinks OBS "+str(nb_linksOBS)+"\n")
#print("Nblinks TRAINING : "+str(nb_linksTRAINING))
sys.stdout.write("Nblinks PRED C0 "+str(nb_linksPRED)+"\n")
nb_linksPREDC1,nb_linksPREDC2,nb_linksPREDC3=0,0,0

for link in predtimes:
	if link in sc1._pair_set:
		nb_linksPREDC1 += len(predtimes[link])
	elif link in sc2._pair_set:
		nb_linksPREDC2 += len(predtimes[link])
	elif link in sc3._pair_set:
		nb_linksPREDC3 += len(predtimes[link])

sys.stdout.write("Nblinks PRED C1 "+str(nb_linksPREDC1)+"\n")
sys.stdout.write("Nblinks PRED C2 "+str(nb_linksPREDC2)+"\n")
sys.stdout.write("Nblinks PRED C3 "+str(nb_linksPREDC3)+"\n")

nb_linksPredictedC01,nb_linksPredictedC02,nb_linksPredictedC03=0,0,0
for link in sc._ranks:
	if link in sc1._pair_set:
		nb_linksPredictedC01 += sc._ranks[link]
	elif link in sc2._pair_set:
		nb_linksPredictedC02 += sc._ranks[link]
	elif link in sc3._pair_set:
		nb_linksPredictedC03 += sc._ranks[link]

#print("Activity predicted : "+str(float(n)/(tendpred-tstartpred)))
sys.stdout.write("Nblinks predicted C0 "+str(n)+"\n")
sys.stdout.write("Nblinks predicted C01 "+str(nb_linksPredictedC01)+"\n")
sys.stdout.write("Nblinks predicted C02 "+str(nb_linksPredictedC02)+"\n")
sys.stdout.write("Nblinks predicted C03 "+str(nb_linksPredictedC03)+"\n")

nb_linksPredictedC1,nb_linksPredictedC2,nb_linksPredictedC3=0,0,0
for link in sc._ranks:
	if link in sc1._pair_set:
		nb_linksPredictedC1 += scPLUS._ranks[link]
	elif link in sc2._pair_set:
		nb_linksPredictedC2 += scPLUS._ranks[link]
	elif link in sc3._pair_set:
		nb_linksPredictedC3 += scPLUS._ranks[link]

sys.stdout.write("Nblinks predicted C1 "+str(nb_linksPredictedC1)+"\n")
sys.stdout.write("Nblinks predicted C2 "+str(nb_linksPredictedC2)+"\n")
sys.stdout.write("Nblinks predicted C3 "+str(nb_linksPredictedC3)+"\n")

sys.stdout.write("Activity predicted "+str(float(n)/(tendpred-tstartpred))+"\n")
sys.stdout.write("Real activity "+str(float(nb_linksPRED)/(tendpred-tstartpred))+"\n")

sys.stdout.write("Nbpairs C0 "+str(len(scPLUS._ranks))+"\n")
sys.stdout.write("Nbpairs C1 "+str(len(sc1._ranks))+"\n")
sys.stdout.write("Nbpairs C2 "+str(len(sc2._ranks))+"\n")
sys.stdout.write("Nbpairs C3 "+str(len(sc3._ranks))+"\n")



sys.stdout.write("C0{\n")

for item in sorted(predconfmetric.items(),key=itemgetter(1),reverse=True):

	sys.stdout.write(str(item[0])+" "+ str(item[1])+"\n")
sys.stdout.write("}\n")#sc.traceScorehistogram(50)

sys.stdout.write("C1{\n")

for item in sorted(predconfmetric1.items(),key=itemgetter(1),reverse=True):

	sys.stdout.write(str(item[0])+" "+ str(item[1])+"\n")
sys.stdout.write("}\n")#sc.traceScorehistogram(50)

sys.stdout.write("C2{\n")

for item in sorted(predconfmetric2.items(),key=itemgetter(1),reverse=True):

	sys.stdout.write(str(item[0])+" "+ str(item[1])+"\n")
sys.stdout.write("}\n")#sc.traceScorehistogram(50)

sys.stdout.write("C3{\n")

for item in sorted(predconfmetric3.items(),key=itemgetter(1),reverse=True):

	sys.stdout.write(str(item[0])+" "+ str(item[1])+"\n")
sys.stdout.write("}\n")#sc.traceScorehistogram(50)

ev = evaluate()
ev01 = evaluate()
ev02 = evaluate()
ev03 = evaluate()
# ev.calculateScore(sc._ranks,predtimes)
# ev01.calculateScore({x:sc._ranks[x] for x in sc1._ranks},predtimes)
# ev02.calculateScore({x:sc._ranks[x] for x in sc2._ranks},predtimes)
# ev03.calculateScore({x:sc._ranks[x] for x in sc3._ranks},predtimes)

ev.calculateScoreFromTimeAggreg(sc._ranks,predtimesaggregated)
ev01.calculateScoreFromTimeAggreg({x:sc._ranks[x] for x in sc1._ranks},predtimesaggregated)
ev02.calculateScoreFromTimeAggreg({x:sc._ranks[x] for x in sc2._ranks},predtimesaggregated)
ev03.calculateScoreFromTimeAggreg({x:sc._ranks[x] for x in sc3._ranks},predtimesaggregated)

sys.stdout.write("C0:\n")
ev.printeval()

sys.stdout.write("C0_1:\n")
ev01.printeval()

sys.stdout.write("C0_2:\n")
ev02.printeval()

sys.stdout.write("C0_3:\n")
ev03.printeval()

evPLUS = evaluate()
evPLUS.calculateScore(scPLUS._ranks,predtimes)
sys.stdout.write("CPLUS:\n")
evPLUS.printeval()

ev1 = evaluate()
ev2 = evaluate()
ev3 = evaluate()

# ev1.calculateScore({x:scPLUS._ranks[x] for x in sc1._ranks},predtimes)
# ev2.calculateScore({x:scPLUS._ranks[x] for x in sc2._ranks},predtimes)
# ev3.calculateScore({x:scPLUS._ranks[x] for x in sc3._ranks},predtimes)

ev1.calculateScoreFromTimeAggreg({x:scPLUS._ranks[x] for x in sc1._ranks},predtimesaggregated)
ev2.calculateScoreFromTimeAggreg({x:scPLUS._ranks[x] for x in sc2._ranks},predtimesaggregated)
ev3.calculateScoreFromTimeAggreg({x:scPLUS._ranks[x] for x in sc3._ranks},predtimesaggregated)

sys.stdout.write("C1:\n")
ev1.printeval()

sys.stdout.write("C2:\n")
ev2.printeval()

sys.stdout.write("C3:\n")
ev3.printeval()


# subC1=ev1.CumulTp({x:scPLUS._ranks[x] for x in sc1._ranks},predtimes)
# plt.subplot(4, 2, 1)
# n, bins, patches= plt.hist(subC1,50, histtype='step',cumulative=True)
# plt.title("C1")
#
# subC2=ev2.CumulTp({x:scPLUS._ranks[x] for x in sc2._ranks},predtimes)
# plt.subplot(4, 2, 3)
# n, bins, patches= plt.hist(subC2,50, histtype='step',cumulative=True)
# plt.title("C2")
#
# subC3=ev3.CumulTp({x:scPLUS._ranks[x] for x in sc3._ranks},predtimes)
# plt.subplot(4, 2, 5)
# n, bins, patches= plt.hist(subC3,50, histtype='step',cumulative=True)
# plt.title("C3")
#
# subPLUS=evPLUS.CumulTp(Mergeranks,predtimes)
# plt.subplot(4, 2, 7)
# n, bins, patches= plt.hist(subPLUS,50, histtype='step',cumulative=True)
# plt.title("PLUS")
#
# subC01=ev01.CumulTp({x:sc._ranks[x] for x in sc1._ranks},predtimes)
# plt.subplot(4, 2, 2)
# n, bins, patches= plt.hist(subC01,50, histtype='step',cumulative=True)
# plt.title("C01")
#
# subC02=ev1.CumulTp({x:sc._ranks[x] for x in sc2._ranks},predtimes)
# plt.subplot(4, 2, 4)
# n, bins, patches= plt.hist(subC02,50, histtype='step',cumulative=True)
# plt.title("C02")
#
# subC03=ev1.CumulTp({x:sc._ranks[x] for x in sc3._ranks},predtimes)
# plt.subplot(4, 2, 6)
# n, bins, patches= plt.hist(subC03,50, histtype='step',cumulative=True)
# plt.title("C03")
#
# subC0=ev.CumulTp(sc._ranks,predtimes)
# plt.subplot(4, 2, 8)
# n, bins, patches= plt.hist(subC0,50, histtype='step',cumulative=True)
# plt.title("C0")
#
#
# plt.show()







#
