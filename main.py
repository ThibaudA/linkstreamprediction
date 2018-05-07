import sys
import numpy as np
from metrics import metrics
from evaluation import evaluate
from scoring import score
from classes import classes
from math import floor
import itertools
import matplotlib.pyplot as plt
import operator
from operator import itemgetter, attrgetter
import os

times = dict()  #Links ObsT+PredT+Obs
predtimes=dict() #Links Pred
pairclasses = classes()

metrics= metrics()
Extract = False
OnePred = False
pairclasses._classthreshold = 5
threshold = True
# UPGMA = False
UPGMAINV = False
UPGMASIZE = False
#Number of step of random explo without classes
RENbstep =1000
#Number of step of random explo with classes
REPNbstep=1000
#Maximum number of step during gradient descent without classes
GDMaxstep=1000
#Maximum number of step during gradient descent with classes
GDPMaxstep=1000
#Gradient descent parameters
#derivation step
derstep = 0.05
#lenght of a step during exploration of parameter space
sizelinexpstep = 0.05
#Number of step in the same direction
numlinexpstep = 100

if len(sys.argv)!=2:
	sys.stderr.write("0  #start time of TrainingObservation\n")
	sys.stderr.write("100 #end time of TrainingObservation\n")

	sys.stderr.write("100 #start time of TrainingPrediction\n")
	sys.stderr.write("150 #end time of TrainingPrediction\n")

	sys.stderr.write("100  #start time of Observation\n")
	sys.stderr.write("150 #end time of Observation\n")

	sys.stderr.write("150 #start time of Prediction\n")
	sys.stderr.write("200 #end time of Prediction\n")

	sys.stderr.write("Metrics #Metrics used\n")
	sys.stderr.write("PairActivityExtrapolation\n")
	sys.stderr.write("commonNeighbors\n")
	sys.stderr.write("EndMetrics\n")

	sys.stderr.write("Commentaries:\n")

	sys.stderr.write("Bla bla \n")
	exit(1)
else:
	conf = open(sys.argv[1], 'r')
	tstartobsT = float(conf.readline().split("#")[0].strip(" "))  #start time of Trainingobservation
	tendobsT=float(conf.readline().split("#")[0].strip(" ")) #end time of Trainingobservation
	tstartpredT =  float(conf.readline().split("#")[0].strip(" "))  #start time of training Pred
	tendpredT = float(conf.readline().split("#")[0].strip(" "))  #end time of training Pred

	tstartobs = float(conf.readline().split("#")[0].strip(" "))  #start time of observation
	tendobs=float(conf.readline().split("#")[0].strip(" ")) #end time of observation
	tstartpred =  float(conf.readline().split("#")[0].strip(" ")) 	#start time of Pred
	tendpred = float(conf.readline().split("#")[0].strip(" "))  #end time of Pred

	sc=score()

	MetricsOK = False
	sys.stdout.write(conf.readline().split("#")[0].strip(" ") + ":\n")
	while MetricsOK != True:    #Read metrics
		line = conf.readline().rstrip("\n").rstrip(" ")
		if line != "EndMetrics":
			if len(line.split(" "))!=1: # if one or more parameter
				metrics._confmetrics[line.split(" ")[0]]=list(map(float,line.split(" ")[1].split(",")))
			else:
				metrics._confmetrics[line.split(" ")[0]]=[0,1.]  # Default Values
		else:
			MetricsOK=True
sys.stdout.write(str(metrics._confmetrics)+"\n")
while line.rstrip("\n") !="Commentaries:":   #Other Options
	line = conf.readline()
	if line.split(" ")[0].rstrip("\n") == "Extract":  #Extract prediction infos in ExtractDirectory
		ExtractDirectory=line.split(" ")[1].rstrip("\n")
		Extract = True
		sys.stdout.write("ExtractDirectory = "+ExtractDirectory)
		dir = os.path.dirname(ExtractDirectory+"/")
		try:
			os.stat(dir)
		except:
			os.mkdir(dir)
	if line.split(" ")[0].rstrip("\n") == "Threshold": #One prediction with given parameters
		pairclasses._classthreshold=float(line.split(" ")[1].rstrip("\n"))

	if line.split(" ")[0].rstrip("\n") == "UPGMAINV": #One prediction with given parameters
		UPGMAINV=True
		threshold =False
		pairclasses._nbcluster=int(line.split(" ")[1].rstrip("\n"))
		pairclasses._VandPparameter=float(line.split(" ")[2].rstrip("\n"))

	if line.split(" ")[0].rstrip("\n") == "UPGMASIZE": #One prediction with given parameters
		UPGMASIZE=True
		threshold =False
		pairclasses._nbcluster=int(line.split(" ")[1].rstrip("\n"))
		pairclasses._VandPparameter=float(line.split(" ")[2].rstrip("\n"))

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

while t<tstartobsT:   #Go to the start
	line = sys.stdin.readline()
	contents = line.split(" ")
	t = float(contents[0])

sys.stderr.write("Starting mesure at: "+str(t)+"\n")
while t<tendpred:
	line = sys.stdin.readline()
	contents = line.split(" ")
	t = float(contents[0])
	if (tstartobsT<=t<tendobsT) or (tstartpredT<=t<tendpredT) or (tstartobs<=t<tendobs):  #Saving usefull links
		u = int(contents[1])
		v = int(contents[2])
		link= frozenset([u,v])
		if not link in times:
			times[link] = []
		times[link].append(t)

	if tstartpred<=t<tendpred: #Saving Ground Truth
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

nb_linksTRAININGAll=0
obstimes=dict()
trainingtimes=dict()
for link in times:  #Creating the Dicts for the learning periods
	obstimes[link]=[x for x in times[link] if x>=tstartobsT and x<tendobsT]
	if len(obstimes[link])==0:
		del obstimes[link]
	trainingtimes[link]=[x for x in times[link] if x>=tstartpredT and x<tendpredT]
	if len(trainingtimes[link])==0:
		del trainingtimes[link]

obsnodes=dict() #Creating dict with the relation between nodes
for link in obstimes:
	u,v = link
	if u not in obsnodes:
		obsnodes[u]=set()
	if v not in obsnodes:
		obsnodes[v]=set()
	obsnodes[u].add(v)
	obsnodes[v].add(u)
	nb_linksOBS1 = nb_linksOBS1 + len([x for x in obstimes[link] if x>=tstartobsT and x<(tendobsT+tstartobsT)/2]) #Usefull for some extrapolation methods
	nb_linksOBS2 = nb_linksOBS2 + len([x for x in obstimes[link] if x>=(tendobsT+tstartobsT)/2 and x<tendobsT])
	nb_linksOBS=nb_linksOBS1+nb_linksOBS2

if Extract: #Extract the usefull parts of the dataset
	score.extractTime(obstimes,ExtractDirectory+ "/ExtractOBS")
	score.extractTime(trainingtimes,ExtractDirectory+ "/ExtractTRAIN")



trainingtimesaggregated=dict() #Creating a Dict for faster prediction evaluation
for link in trainingtimes:
	nb_linksTRAININGAll = nb_linksTRAININGAll + len(trainingtimes[link])
	trainingtimesaggregated[link]= len(trainingtimes[link])

sys.stdout.write("TRAINING:\n")

sys.stdout.write("Nblinks OBS "+str(nb_linksOBS)+"\n")
sys.stdout.write("Nblinks TRAINING C0 "+str(nb_linksTRAININGAll)+"\n")

#Class Making
#3 Class : C1 = New link C2 = less than classthreshold link C3 more than classthreshold






# pairclasses._classthreshold = 5
# pairclasses.classbythreshold(obstimes,obsnodes)

# pairclasses._VandPparameter=1/((tendobsT-tstartobsT)/3)
# pairclasses._VandPparameter=0
# pairclasses._nbcluster=2


if UPGMAINV:
	pairclasses.classbyUPGMA(obstimes,trainingtimes,obsnodes)
elif UPGMASIZE:
	pairclasses.classbyUPGMASIZE(obstimes,trainingtimes,obsnodes)
else:
	pairclasses.classbythreshold(obstimes,obsnodes)

nb_linksTRAINING=pairclasses.getnblinksTraining(trainingtimes)


for u,v in itertools.combinations(obsnodes.keys(),2): #to predict new pair of nodes and initialize the classes
	link = frozenset([u,v])
	sc.addPair(link)

for classID in pairclasses._classorder:
	sys.stdout.write("Nblinks TRAINING "+ classID +" "+str(nb_linksTRAINING[classID])+"\n")

sys.stdout.write("Nbpairs C0 "+str(len(pairclasses._classUnion._pair_set))+"\n")
for classID in pairclasses._classorder:
	sys.stdout.write("Nbpairs "+ classID+" "+str(len(pairclasses._classscore[classID]._pair_set))+"\n")

#Compute metrics, do the integration, compute the maximum of each metric and normalize each metric  for each pair
#ALL
metrics.computeMetrics(sc,tstartobsT,tendobsT,obstimes,obsnodes) #compute all metrics
sc.integrateMetrics(tstartpredT,tendpredT) #integrate metrics
# sc.correlationMatrix(metrics._confmetrics)
# sys.exit()
sc.setMaxByMetric()  #Normalisation
sc.normalizeMetrics()
if Extract:
	sc.extractMetric(metrics._confmetrics,ExtractDirectory+ "/ExtractMetrics")


pairclasses.computeMetrics(metrics,tstartobsT,tendobsT,tstartpredT,tendpredT,obstimes,obsnodes) #compute all metrics for all classes

#extrapolate the activity

# n=metrics.linearActivityExtrapolation(nb_linksOBS,tstartobsT,tendobsT,tstartpredT,tendpredT)
#n=metrics.fitnPointrActivityExtrapolation(obstimes,tstart,tendobs,tmesure,tendtraining,30)
# n=metrics.twopointrActivityExtrapolation(nb_linksOBS1,nb_linksOBS2,tstart,(tstart+tendobs)/2,tendobs,tmesure,tendtraining)
#Triche
n= nb_linksTRAININGAll
print(n)

if OnePred: #Making one prediction using the parameters in the config file
	sc.OnePred(tstartobsT,tendobsT,tstartpredT,tendpredT,n,obstimes,trainingtimesaggregated,metrics._confmetrics)


#Random exploration for gradient descent initialisation
initconfmetrics = sc.randomExplo(tstartobsT,tendobsT,tstartpredT,tendpredT,n,trainingtimesaggregated,metrics._confmetrics,RENbstep)
sys.stdout.write("End init "+str(initconfmetrics)+" \n")
predconfmetric, Finalscore =sc.gradDescentLinExp(tstartobsT,tendobsT,tstartpredT,tendpredT,n,trainingtimesaggregated,initconfmetrics,derstep,sizelinexpstep,numlinexpstep,GDMaxstep)
sys.stdout.write("C0 Done\n")

initconfmetrics = score.randomExploClasses(tstartobsT,tendobsT,tstartpredT,tendpredT,n,trainingtimesaggregated,metrics._confmetrics,REPNbstep,pairclasses)

# initconfmetrics1,initconfmetrics2,initconfmetrics3 = scPLUS.randomExploPLUS(tstartobsT,tendobsT,tstartpredT,tendpredT,n,trainingtimesaggregated,metrics._confmetrics,REPNbstep,sc1,sc2,sc3)
#
for classID in pairclasses._classorder:
	sys.stdout.write("End init "+ classID +" "+str(initconfmetrics[classID])+" \n")


#perform gradient descent to better tune the parameters

predconfmetricClasses,FinalscoreUnion,FinalscoreClasses=score.gradDescentLinExpClasses(tstartobsT,tendobsT,tstartpredT,tendpredT,n,trainingtimesaggregated,initconfmetrics,derstep,sizelinexpstep,numlinexpstep,GDPMaxstep,pairclasses)
sys.stdout.write("C123 Done\n")



if Extract: #extract the learing results
	score.extractCoef(predconfmetric,predconfmetricClasses,ExtractDirectory+ "/ExtractCoefs",pairclasses._classorder)
	sc.extractPrediction(ExtractDirectory+ "/ExtractPredC0")
	for classID in pairclasses._classorder:
		pairclasses._classscore[classID].extractPrediction(ExtractDirectory+ "/ExtractPred"+classID)

#Compute the total number of link predicted in each classes in the final combination without classes

nb_linksPredictedWOclasses =dict()
for classID in pairclasses._classorder:
	nb_linksPredictedWOclasses[classID]=0

for link in sc._ranks:
	for classID in pairclasses._classorder:
		if link in pairclasses._classscore[classID]._pair_set:
			nb_linksPredictedWOclasses[classID] += sc._ranks[link]

sys.stdout.write("Nblinks predicted C0 "+str(n)+"\n")
for classID in pairclasses._classorder:
	sys.stdout.write("Nblinks predicted C0" +classID[1:] +" " +str(nb_linksPredictedWOclasses[classID])+"\n")

#Compute the total number of link predicted in each classes in the final combination with classes

nb_linksPredicted =dict()
for classID in pairclasses._classorder:
	nb_linksPredicted[classID]=0

for link in sc._ranks:
	for classID in pairclasses._classorder:
		if link in pairclasses._classscore[classID]._pair_set:
			nb_linksPredicted[classID] += pairclasses._classUnion._ranks[link]

for classID in pairclasses._classorder:
	sys.stdout.write("Nblinks predicted " +classID +" " +str(nb_linksPredicted[classID])+"\n")


#Compute and print the evaluation
ev0=dict()
for classID in pairclasses._classorder:
	ev0[classID] = evaluate()
	ev0[classID].calculateScore({x:sc._ranks[x] for x in pairclasses._classscore[classID]._ranks},trainingtimes)

if Extract: #extract prediction evaluation
	evaluate.extractQualitybypair(sc._ranks,trainingtimes,ExtractDirectory+ "/ExtractQualitybypairC0")
	for classID in pairclasses._classorder:
		evaluate.extractQualitybypair(pairclasses._classscore[classID]._ranks,trainingtimes,ExtractDirectory+ "/ExtractQualitybypair"+classID)


sys.stdout.write("C0: \n")
Finalscore.printeval()
for classID in pairclasses._classorder:
	sys.stdout.write("C0_"+classID[1:]+": \n")
	ev0[classID].printeval()

sys.stdout.write("C123: \n")
FinalscoreUnion.printeval()

for classID in pairclasses._classorder:
	sys.stdout.write(classID+": \n")
	FinalscoreClasses[classID].printeval()


sys.stdout.write("End train "+str(predconfmetric)+" "+str(Finalscore._F)+"\n")
for classID in pairclasses._classorder:
	sys.stdout.write("End train " +classID + " "+str(predconfmetricClasses[classID])+" "+str(FinalscoreClasses[classID]._F)+"\n")

#End Training Start Prediction
sys.stdout.write("PREDICTION\n")

nb_linksOBS=0
nb_linksOBS1=0
nb_linksOBS2=0
obstimesTforUPGMA=obstimes.copy()
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


sc.resetPairs() #making sure sc is clear
sc.resetRanks()

pairclasses.resetclasslists()

if UPGMAINV:
	pairclasses.MatchclassbyUPGMA(obstimes,obsnodes,obstimesTforUPGMA,tstartobs,tendobs,tstartobsT,tendobsT)
elif UPGMASIZE:
	pairclasses.MatchclassbyUPGMASIZE(obstimes,obsnodes,obstimesTforUPGMA,tstartobs,tendobs,tstartobsT,tendobsT)
else:
	pairclasses.classbythreshold(obstimes,obsnodes)


for u,v in itertools.combinations(obsnodes.keys(),2): #to predict new pair of nodes
	link = frozenset([u,v])
	sc.addPair(link)


# n=nb_linksPRED
#n=metrics.twopointrActivityExtrapolation(nb_linksOBS1,nb_linksOBS2,tstartobs,(tstartobs+tendobs)/2,tendobs,tstartpred,tendpred)
n=metrics.linearActivityExtrapolation(nb_linksOBS,tstartobs,tendobs,tstartpred,tendpred)

metrics.computeMetrics(sc,tstartobs,tendobs,obstimes,obsnodes)
sc.integrateMetrics(tstartpred,tendpred)
sc.setMaxByMetric()
sc.normalizeMetrics()
sc.rankPairs(tstartpred,tendpred,predconfmetric)
sc.normalizeranksbyintegral(n)





pairclasses.computeMetrics(metrics,tstartobs,tendobs,tstartpred,tendpred,obstimes,obsnodes) #compute all metrics for all classes

for classID in pairclasses._classscore:
    pairclasses._classscore[classID].rankPairs(tstartpred,tendpred,predconfmetricClasses[classID])
Mergeranks=dict()
for classID in pairclasses._classscore.keys():
    Mergeranks.update(pairclasses._classscore[classID]._ranks.copy())
pairclasses._classUnion._ranks=Mergeranks
pairclasses._classUnion.normalizeranksbyintegral(n)



sys.stdout.write("Nblinks OBS "+str(nb_linksOBS)+"\n")
sys.stdout.write("Nblinks PRED C0 "+str(nb_linksPRED)+"\n")

nb_linksPREDClasses=dict()
for classID in pairclasses._classorder:
	nb_linksPREDClasses[classID]=0

for link in predtimes:
	for classID in pairclasses._classorder:
		if link in pairclasses._classscore[classID]._pair_set:
			nb_linksPREDClasses[classID] += len(predtimes[link])
for classID in pairclasses._classorder:
	sys.stdout.write("Nblinks PRED "+ classID + " " +str(nb_linksPREDClasses[classID])+"\n")

nb_linksPredictedC01,nb_linksPredictedC02,nb_linksPredictedC03=0,0,0
nb_linksPredictedWOclasses=dict()
for classID in pairclasses._classorder:
	nb_linksPredictedWOclasses[classID]=0
for link in sc._ranks:
	for classID in pairclasses._classorder:
		if link in pairclasses._classscore[classID]._pair_set:
			nb_linksPredictedWOclasses[classID] += sc._ranks[link]

sys.stdout.write("Nblinks predicted C0 "+str(n)+"\n")
for classID in pairclasses._classorder:
	sys.stdout.write("Nblinks predicted C0"+classID[1:] + " "+str(nb_linksPredictedWOclasses[classID])+"\n")

nb_linksPredictedClasses = dict()
for classID in pairclasses._classorder:
	nb_linksPredictedClasses[classID]=0


for link in sc._ranks:
	for classID in pairclasses._classorder:
		if link in pairclasses._classscore[classID]._pair_set:
			nb_linksPredictedClasses[classID] += pairclasses._classUnion._ranks[link]

for classID in pairclasses._classorder:
	sys.stdout.write("Nblinks predicted "+classID+" "+str(nb_linksPredictedClasses[classID])+"\n")

sys.stdout.write("Activity predicted "+str(float(n)/(tendpred-tstartpred))+"\n")
sys.stdout.write("Real activity "+str(float(nb_linksPRED)/(tendpred-tstartpred))+"\n")

sys.stdout.write("Nbpairs C0 "+str(len(pairclasses._classUnion._ranks))+"\n")
for classID in pairclasses._classorder:
	sys.stdout.write("Nbpairs "+ classID+" "+str(len(pairclasses._classscore[classID]._ranks))+"\n")



sys.stdout.write("C0{\n")
#print the metric coefs
for item in sorted(predconfmetric.items(),key=itemgetter(1),reverse=True):

	sys.stdout.write(str(item[0])+" "+ str(item[1])+"\n")
sys.stdout.write("}\n")

for classID in pairclasses._classorder:
	sys.stdout.write(classID+"{\n")
	for item in sorted(predconfmetricClasses[classID].items(),key=itemgetter(1),reverse=True):

		sys.stdout.write(str(item[0])+" "+ str(item[1])+"\n")
	sys.stdout.write("}\n")


ev = evaluate()

ev.calculateScoreFromTimeAggreg(sc._ranks,predtimesaggregated)
sys.stdout.write("C0:\n")
ev.printeval()

for classID in pairclasses._classorder:
	ev0=evaluate()
	ev0.calculateScoreFromTimeAggreg({x:sc._ranks[x] for x in pairclasses._classscore[classID]._ranks},predtimesaggregated)
	sys.stdout.write("C0_"+classID[1:]+":\n")
	ev0.printeval()


evUnion = evaluate()
evUnion.calculateScore(pairclasses._classUnion._ranks,predtimes)
sys.stdout.write("C123:\n")
evUnion.printeval()


for classID in pairclasses._classorder:
	ev1 = evaluate()
	ev1.calculateScoreFromTimeAggreg({x:pairclasses._classUnion._ranks[x] for x in pairclasses._classscore[classID]._ranks},predtimesaggregated)

	sys.stdout.write(classID+":\n")
	ev1.printeval()























#
