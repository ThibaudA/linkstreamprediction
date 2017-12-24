import numpy as np
from scipy.optimize import curve_fit
import sys
import math
import bisect
import matplotlib as mpl
import matplotlib.pyplot as plt
class metrics:
    def __init__(self):
        self._confmetrics = dict()
        self._TP = 0


    def computeMetrics(self,sc,tstart,t,times,nodes): #t=end obs

        for metricsname in self._confmetrics: #launch each metrics in confmetrics

            if metricsname == "benchMark":
                for link in sc._pair:
                    u,v=link
                    if link in times:
                        sc.addFunction(link,"benchMark",self.benchMark(times[link]))

            elif metricsname[:21] == "benchMarkReduxNbLinks":
                n=int(metricsname[21:])
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link]) > n:
                        sc.addFunction(link,metricsname,self.benchMarkReduxNbLinks(times[link],t,n))
                    elif len(times[link]) > 1:
                        sc.addFunction(link,metricsname,self.benchMarkReduxNbLinks(times[link],t,len(times[link])))

            elif metricsname[:23] == "benchMarkReduxTimeInter":
                n=int(metricsname[23:])
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link]) > 0:
                        sc.addFunction(link,metricsname,self.benchMarkReduxTimeInter(times[link],t,n))

            elif metricsname== "twopointExtrapolation":
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link]) > 0:
                        sc.addFunction(link,metricsname,self.twopointExtrapolation(times[link],tstart,t))

            elif metricsname[:22]== "fitnPointExtrapolation":
                n=int(metricsname[22:])
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link]) > 0:
                        sc.addFunction(link,metricsname,self.fitnPointExtrapolation(times[link],tstart,t,n))

            elif metricsname == "intercontactTimes":
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link])>1:
                        sc.addFunction(link,"intercontactTimes",self.intercontactTimes(times[link]))
                        #sc.addGaussian(link,var,mean,times[link][-1],1)

            elif metricsname[:22] == "intercontactTimesRedux":
                n=int(metricsname[22:])
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link])>n:
                        sc.addFunction(link,metricsname,self.intercontactTimesRedux(times[link],n))
                    elif len(times[link])>1:
                        sc.addFunction(link,metricsname,self.intercontactTimes(times[link]))
                        #sc.addGaussian(link,var,mean,times[link][-1],1)


            elif metricsname == "commonNeighbors":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"commonNeighbors",self.commonNeighbors(nodes[u],nodes[v]))

                    # if self._confmetrics[metricsname] is not None:
                    #     sc.addOffSet(link,self.commonNeighbors(nodes[u],nodes[v])*self._confmetrics[metricsname][0])
                    # else:
                    #     sc.addOffSet(link,self.commonNeighbors(nodes[u],nodes[v]))

            elif metricsname[:23] == "exponentialInterContact":
                n=int(metricsname[23:])
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    if len(times[link])>n:
                        sc.addFunction(link,metricsname,self.exponentialInterContact(times[link],n))
                    elif len(times[link])>2:
                        sc.addFunction(link,metricsname,self.exponentialInterContact(times[link],2))
                        #sc.addGaussian(link,var,mean,times[link][-1],1)

            elif metricsname == "exponentialLast":
                for link in sc._pair:
                    u,v=link
                    if link not in times:
                        continue
                    sc.addFunction(link,"exponentialLast",self.exponentialLast(times[link],t))

            elif metricsname == "jaccardIndex":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"jaccardIndex",self.jaccardIndex(nodes[u],nodes[v]))

            elif metricsname == "weightedCommonNeighbors":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"weightedCommonNeighbors",self.weightedCommonNeighbors(u,v,times,nodes[u],nodes[v]))

                # if self._confmetrics[metricsname] is not None:
                #     sc.addOffSet(link,self.weightedCommonNeighbors(u,v,times,nodes[u],nodes[v])*self._confmetrics[metricsname][0])
                # else:
                #     sc.addOffSet(link,self.weightedCommonNeighbors(u,v,times,nodes[u],nodes[v]))

            elif metricsname == "resourceAlloc":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"resourceAlloc",self.resourceAlloc(u,v,nodes))

                #
                # if self._confmetrics[metricsname] is not None:
                #     sc.addOffSet(link,self.resourceAlloc(u,v,nodes)*self._confmetrics[metricsname][0])
                # else:
                #     sc.addOffSet(link,self.resourceAlloc(u,v,nodes))
            elif metricsname == "weightedResourceAlloc":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"weightedResourceAlloc",self.weightedResourceAlloc(u,v,times,nodes))

                # if self._confmetrics[metricsname] is not None:
                #     sc.addOffSet(link,self.weightedResourceAlloc(u,v,times,nodes)*self._confmetrics[metricsname][0])
                # else:
                #     sc.addOffSet(link,self.weightedResourceAlloc(u,v,times,nodes))
            elif metricsname == "adamicAdar":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"adamicAdar",self.adamicAdar(u,v,nodes))

                # if self._confmetrics[metricsname] is not None:
                #     sc.addOffSet(link,self.adamicAdar(u,v,nodes)*self._confmetrics[metricsname][0])
                # else:
                #     sc.addOffSet(link,self.adamicAdar(u,v,nodes))
            elif metricsname == "weightedAdamicAdar":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"weightedAdamicAdar",self.weightedAdamicAdar(u,v,times,nodes))

                # if self._confmetrics[metricsname] is not None:
                #         sc.addOffSet(link,self.weightedAdamicAdar(u,v,times,nodes)*self._confmetrics[metricsname][0])
                # else:
                #         sc.addOffSet(link,self.weightedAdamicAdar(u,v,times,nodes))
            elif metricsname == "sorensenIndex":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"sorensenIndex",self.sorensenIndex(u,v,nodes))

                # if self._confmetrics[metricsname] is not None:
                #     sc.addOffSet(link,self.sorensenIndex(u,v,nodes)*self._confmetrics[metricsname][0])
                # else:
                #     sc.addOffSet(link,self.sorensenIndex(u,v,nodes))
            elif metricsname == "weightedSorensenIndex":
                for link in sc._pair:
                    u,v=link
                    sc.addFunction(link,"weightedSorensenIndex",self.weightedSorensenIndex(u,v,times,nodes))

                # if self._confmetrics[metricsname] is not None:
                #     sc.addOffSet(link,self.weightedSorensenIndex(u,v,times,nodes)*self._confmetrics[metricsname][0])
                # else:
                #     sc.addOffSet(link,self.weightedSorensenIndex(u,v,times,nodes))
            elif metricsname == "motif1":
                self.motif1(nodes,times)
                    #sc.addFunction(link,"weightedSorensenIndex",self.weightedSorensenIndex(u,v,times,nodes))

            else:
                sys.stderr.write("-- WARNING: metric Not Found: "+ metricsname+"--\n" )



    def benchMark(self,time):
        s = len(time)
        return lambda t: s

    def benchMarkReduxNbLinks(self,time,t,n):
        s = len(time[-n:])/(float(t-time[-n]))
        # if time[-n]<50:
        #     print "blaa"
        # else:
        #     print "OK"
        return lambda t: s

    def benchMarkReduxTimeInter(self,time,t,n):
        # s = len(time[-n:])/(float(t-time[-n]))
        nlinks=len([x for x in time if x>t-n and x<=t])
        # print("nlinks:" +str(nlinks))
        # print("n:"+str(n))

        # print("nl/n:"+str(nlinks/float(n)))

        # if time[-n]<50:
        #     print "blaa"
        # else:
        #     print "OK"
        return lambda t: nlinks/n

    def intercontactTimes(self,time):
        itc = np.array([j - i for i,j in zip(time[:-1], time[1:])])
        #print itc
        last=time[-1]
        mean = np.mean(itc)
        var = np.var(itc)
        #THATS UGLY:
        var=var+0.1
        return lambda t: np.exp(-pow((t-last-mean/2)%(mean)-mean/2,2)/(2*pow(var,2)))/(var*math.sqrt(2*math.pi))

    def intercontactTimesRedux(self,time,n):
        # print time[-n:-1], time[-n+1:]
        itc = np.array([j - i for i,j in zip(time[-n:-1], time[-n+1:])])
        #print itc
        last=time[-1]
        mean = np.mean(itc)
        var = np.var(itc)
        # print itc
        #THATS UGLY:
        var=var+0.1
        return lambda t: np.exp(-pow((t-last-mean/2)%(mean)-mean/2,2)/(2*pow(var,2)))/(var*math.sqrt(2*math.pi))

    def exponentialInterContact(self,time,n):
        itc = np.array([j - i for i,j in zip(time[-n:-1], time[-n+1:])])
        #print itc
        last=time[-1]
        mean = np.mean(itc)
        return lambda t: np.exp(-mean)

    def exponentialLast(self,time,t):
        #print itc
        last=float(time[-1])
        print(last)
        return lambda t: np.exp(-(t-last))

    def commonNeighbors(self,nodes_u,nodes_v):
        # print(float(len(nodes_u.intersection(nodes_v))))
        return lambda t: float(len(nodes_u.intersection(nodes_v))) #modif!

    def jaccardIndex(self,nodes_u,nodes_v):
        return lambda t: float(len(nodes_u.intersection(nodes_v)))/len(nodes_u.union(nodes_v)) #modif!



    def weightedCommonNeighbors(self,u,v,times,nodes_u,nodes_v):
        s=0.
        for k in nodes_u.intersection(nodes_v):
            s+=float(len(times[frozenset([u,k])])*len(times[frozenset([v,k])]))
        return lambda t:s

    def resourceAlloc(self,u,v,nodes):
        s=0.
        for k in nodes[u].intersection(nodes[v]):
            s+=1/float(len(nodes[k]))
        return lambda t:s
    def weightedResourceAlloc(self,u,v,times,nodes):
        s=0.
        for k in nodes[u].intersection(nodes[v]):
            W=0
            for j in nodes[k]:
                W += len(times[frozenset([j,k])])
            s+=1/float(W)
        return lambda t:s

    def adamicAdar(self,u,v,nodes):
        s=0.
        for k in nodes[u].intersection(nodes[v]):
            s+=1/math.log(len(nodes[k]))
        return lambda t:s

    def weightedAdamicAdar(self,u,v,times,nodes):
        s=0.
        for k in nodes[u].intersection(nodes[v]):
            W=0
            for j in nodes[k]:
                W += len(times[frozenset([j,k])])
            s+=1/math.log(W)
        return lambda t:s


    def sorensenIndex(self,u,v,nodes):
        return  lambda t:2.0*len(nodes[u].intersection(nodes[v]))/(len(nodes[v])+len(nodes[u]))


    def weightedSorensenIndex(self,u,v,times,nodes):
        s=0.
        Wu,Wv=0,0
        for j in nodes[u]:
            Wu+=float(len(times[frozenset([j,u])]))

        for i in nodes[v]:
            Wv+=float(len(times[frozenset([i,v])]))

        for k in nodes[u].intersection(nodes[v]):
            s+= float(len(times[frozenset([u,k])])+len(times[frozenset([v,k])]))
        return lambda t:s/(Wu+Wv)

    def twopointExtrapolation(self,time,tstart,tend):
        tmid=(tstart+tend)/2
        nb_links1=len([x for x in time if x>tstart and x<=tmid])
        nb_links2=len([x for x in time if x>tmid and x<=tend])
        a=2*(nb_links2/(tend-tmid)-nb_links1/(tmid-tstart))/(tend-tstart)
        b=(nb_links1/(tmid-tstart)*(tmid+tend)-nb_links2/(tend-tmid)*(tstart+tmid))/(tend-tstart)
        return lambda t: max(0,a*t+b)

    def fitnPointExtrapolation(self,time,tstart,tendobs,n):

        xedges=list(range(int(tstart),int(tendobs),int((tendobs-tstart)/n)))
        data=[0]*(len(xedges))
        for i in range(len(xedges)):

            data[i]=len([x for x in time if x>xedges[i] and x<=xedges[i]+(tendobs-tstart)/n])
            data[i]=data[i]/((tendobs-tstart)/n)
        popt, pcov = curve_fit(funcdroite,xedges, data)
        a,b=popt

        return lambda t: max(0,a*t+b)


    def motif1(self,nodes,times):
        histt2t1,histt3=[],[]
        motifscore=dict()
        coef =0
        for link in times:
            u,v=link
            commonneighbors=nodes[u].intersection(nodes[v])
            lastt_u,lastt_v = -1,-1
            for neighbor in commonneighbors:
                for t in times[link]:
                    linku,linkv=frozenset([u,neighbor]),frozenset([v,neighbor])
                    indexu=bisect.bisect_left(times[linku],t)-1
                    indexv=bisect.bisect_left(times[linkv],t)-1
                    if indexu >= 0 and indexv >=0:
                        t_u,t_v = times[linku][indexu],times[linkv][indexv]
                        if t_u != lastt_u and t_v != lastt_v:
                            lastt_u,lastt_v = t_u,t_v
                            if abs(t_u-t_v)<300 and min(t-t_u,t-t_v)<300:
                                histt2t1.append(abs(t_u-t_v))
                                histt3.append(min(t-t_u,t-t_v))
                                if not link in motifscore:
                                    motifscore[link]=[0,0] #nb de motif,timelastmotif
                                motifscore[link][0]=motifscore[link][0]+1
                                motifscore[link][1]=max(t_u,t_v)

        H, xedges, yedges = np.histogram2d(histt2t1,histt3,bins=[range(0, 500, 20),range(20, 500, 20)])
        H=H.T

        xedges,yedges=np.meshgrid(xedges[:-1],yedges[:-1])
        data=H.ravel()
        # data = funcmotif((xedges, yedges), 2, 3, 1, 8)
        popt, pcov = curve_fit(funcmotif,(xedges,yedges), data)
        print('bla')
        print(popt)
        print('vla')
        print(pcov)

        # fig = plt.figure(figsize=(7, 3))
        # ax = fig.add_subplot(131, title='imshow: square bins')
        # plt.xlabel("t2-t1")
        # plt.ylabel("t3")
        # plt.imshow(H, interpolation='nearest', origin='low',extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
        #
        # ax = fig.add_subplot(132, title='pcolormesh: actual edges',aspect='equal')
        # X, Y = np.meshgrid(xedges, yedges)
        # ax.pcolormesh(X, Y, H)
        # ax = fig.add_subplot(133, title='NonUniformImage: interpolated',aspect='equal', xlim=xedges[[0, -1]], ylim=yedges[[0, -1]])
        # im = mpl.image.NonUniformImage(ax, interpolation='bilinear')
        # xcenters = (xedges[:-1] + xedges[1:]) / 2
        # ycenters = (yedges[:-1] + yedges[1:]) / 2
        # im.set_data(xcenters, ycenters, H)
        # ax.images.append(im)
        # plt.show()
        plt.xlabel("t2-t1")
        plt.ylabel("t3")
        plt.hist2d(histt2t1,histt3, bins=range(0, 2000, 20))
        plt.colorbar()
        plt.show()



        return motifscore,coef








#ACTIVITY EXTRAPOLATION:
    #same ACTIVITY
    def linearActivityExtrapolation(self,nb_lines,tstart,tmesure,tstartpred,tendpred):
        return float(nb_lines)*(tendpred-tstartpred)/float(tmesure-tstart)
    #extrapolate ACTIVITY with obs and training
    def twopointrActivityExtrapolation(self,nb_linksOBS,nb_linksTRAINING,tstart,tmesure,tendtraining,tstartpred,tendpred):
        a=2*(nb_linksTRAINING/(tendtraining-tmesure)-nb_linksOBS/(tmesure-tstart))/(tendtraining-tstart)
        b=(nb_linksOBS/(tmesure-tstart)*(tmesure+tendtraining)-nb_linksTRAINING/(tendtraining-tmesure)*(tstart+tmesure))/(tendtraining-tstart)
        # print(a,b)
        #print(nb_linksOBS,nb_linksTRAINING)
        return (a*(tstartpred+tendpred)/2+b)*(tendpred-tstartpred)

    def fitnPointrActivityExtrapolation(self,times,tstart,tendobs,tstartpred,tendpred,n):

        xedges=list(range(int(tstart),int(tendobs),int((tendobs-tstart)/n)))
        data=[0]*(len(xedges))
        for i in range(len(xedges)):

            for link in times:
                 data[i]=data[i]+len([x for x in times[link] if x>xedges[i] and x<=xedges[i]+(tendobs-tstart)/n])
            data[i]=data[i]/((tendobs-tstart)/n)
        popt, pcov = curve_fit(funcdroite,xedges, data)
        a,b=popt
        print(xedges)
        print(data)
        print("popt:",a,b)

        return (a*(tstartpred+tendpred)/2+b)*(tendpred-tstartpred)





























def funcmotif(T, A, alpha,B,beta):
    g=A * np.exp(-alpha * T[0]) + B * np.exp(-beta * T[1])
    return g.ravel()
def funcdroite(t,A,B):
    g=A * t+B
    return g
