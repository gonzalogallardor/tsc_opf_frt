import string
import numpy as np
import pdb

#sim_time = 3
#clearing_time = 0.2
deltat = 0.025

rawfile = open('ieee118.raw','r')
line = rawfile.readline()
if '/' in line: line = line[:line.find('/')]
words = line.split(',')
sbase = float(words[1])
comments = [rawfile.readline(),rawfile.readline()]
#sections = ('bus','load','shunt','generator','branch','transformer')

node_counter = 0
bus_counter = 0
bus_name={}; nominal_voltage={}; bus_type={}; voltage={}; busindex={}
while 1:
    line = rawfile.readline()
    if '/' in line: line = line[:line.find('/')]
    words = line.split(',')
    if len(words) == 1 and int(words[0]) == 0: break
    busnumber = int(words[0])
    bus_name[busnumber] = words[1][1:-1]
    nominal_voltage[busnumber] = float(words[2])
    bus_type[busnumber] = int(words[3])
    voltage[busnumber] = complex(float(words[7])*np.cos(float(words[8])*np.pi/180),float(words[7])*np.sin(float(words[8])*np.pi/180))
    busindex[busnumber] = node_counter
    node_counter = node_counter + 1
    bus_counter = bus_counter + 1

total_load=0
pqload={};pload={};qload={};
with open('cargas.txt') as loadfile:
    for line in loadfile:
        words = line.split()
        busnumber = int(words[0])
        p = float(words[1])
        q = float(words[2])
        pqload[busnumber] = complex(p,q)
        pload[busnumber] = p
        qload[busnumber] = q
        total_load+=p
#print"Total load = ", total_load, " MW"
while 1:
    line = rawfile.readline()
    if '/' in line: line = line[:line.find('/')]
    words = line.split(',')
    if len(words) == 1 and int(words[0]) == 0: break
#    busnumber = int(words[0])
#    busid = words[1][1:-1]
#    p = float(words[5])
#    q = float(words[6])-5
#    pqload[(busnumber,busid)] = complex(p,q)
#    pload[busnumber] = p
#    qload[busnumber] = q
#    total_load+=p

while 1:
    line = rawfile.readline()
    if '/' in line: line = line[:line.find('/')]
    words = line.split(',')
    if len(words) == 1 and int(words[0]) == 0: break

total_p_max = 0
total_p_min = 0
a={};b={};c={};
genp={}; genq={}; genbasmva={}; genrxtran={}; gennodeindex={}; generation_buses=[]; generators=[];
genqmax={}; genqmin={}; genpmax={}; genpmin={};
with open('generadores.txt') as genfile:
    for line in genfile:
        if line[0] != '#':
            words = line.split()
            busnumber = int(words[1])
            genid = '1 '
            a[(busnumber,genid)] = float(words[2])
            b[(busnumber,genid)] = float(words[3])
            c[(busnumber,genid)] = float(words[4])
            genpmax[(busnumber,genid)] = float(words[5])
            genpmin[(busnumber,genid)] = float(words[6])
#            genpmin[(busnumber,genid)] = 0
            total_p_max+=float(genpmax[(busnumber,genid)])
            total_p_min+=float(genpmin[(busnumber,genid)])
            genqmax[(busnumber,genid)] = float(words[7])
            genqmin[(busnumber,genid)] = float(words[8])
            genbasmva[(busnumber,genid)] = genpmax[(busnumber,genid)]*1.1
            genrxtran[(busnumber,genid)] = complex(0.0,0.3)
            gennodeindex[(busnumber,genid)] = node_counter
            node_counter = node_counter + 1
            generation_buses.append(busnumber)
            generators.append((busnumber,genid))
#print len(generators), " generadores capaces de generar entre ", total_p_min, " y ", total_p_max, " MW"
genfile.close()

while 1:
    line = rawfile.readline()
    if '/' in line: line = line[:line.find('/')]
    words = line.split(',')
    if len(words) == 1 and int(words[0]) == 0: break
#    busnumber = int(words[0])
#    genid = words[1][1:-1]
#    genp[(busnumber,genid)] = float(words[2])
#    total_p_prog+=float(genp[(busnumber,genid)])
#    genq[(busnumber,genid)] = float(words[3])
#    genqmax[(busnumber,genid)] = float(words[4])
#    genqmin[(busnumber,genid)] = float(words[5])
##    genbasmva[(busnumber,genid)] = float(words[8])
#    genbasmva[(busnumber,genid)] = Sm
##    genrxtran[(busnumber,genid)] = complex(float(words[9]),float(words[10]))
#    genrxtran[(busnumber,genid)] = complex(0.0,0.3)
#    genpmax[(busnumber,genid)] = float(words[16])
#    genpmin[(busnumber,genid)] = float(words[17])
#    gennodeindex[(busnumber,genid)] = node_counter
#    node_counter = node_counter + 1
#    generation_buses.append(busnumber)
#    generators.append((busnumber,genid))
#generators.sort()

branchrx={}; branchgb={}
while 1:
    line = rawfile.readline()
    if '/' in line: line = line[:line.find('/')]
    words = line.split(',')
    if len(words) == 1 and int(words[0]) == 0: break
    busnumber1 = int(words[0])
    busnumber2 = int(words[1])
    branchid = words[2][1:-1]
    branchrx[(busnumber1,busnumber2,branchid)] = complex(float(words[3]),float(words[4]))
    branchgb[(busnumber1,busnumber2,branchid)] = complex(0,float(words[5]))

transfrx12={}
while 1:
    line = rawfile.readline()
    if '/' in line: line = line[:line.find('/')]
    words = line.split(',')
    if len(words) == 1 and int(words[0]) == 0: break
#    while len(words) < 36: words.extend(string.split(rawfile.readline(),','))
    busnumber1 = int(words[0])
    busnumber2 = int(words[1])
    busnumber3 = int(words[2])
    transfid = words[3][1:-1]
    transfrx12[(busnumber1,busnumber2,busnumber2,transfid)] = complex(float(words[20]),float(words[21]))

rawfile.close()

#load_factors = (.4,.6,.8,1.0,1.2)
#load_factors = (1.0,)
load_factor = 1.0
#angle_limits = (30,40,50,60,70,80,90,100)
#angle_limits = (50,)
#angle_limit = 50
#clearing_times = (.1,.15,.2,.25,.3)
#clearing_times_1 = (.14,.16,.18,.20,.22,.24,.26,.28,.3)
#clearing_times_2 = (.14,.16,.18,.20,.22,.24,.26,.28,.3)
clearing_times_1 = (.3,)
clearing_times_2 = (.3,)
#clearing_time_1 = .2
#clearing_time_2 = .2
#sim_times = (1,)
sim_time = 2
#for load_factor in load_factors:
#for sim_time in sim_times:
#    for angle_limit in angle_limits:
#    for clearing_time in clearing_times:
for clearing_time_1 in clearing_times_1:
    for clearing_time_2 in clearing_times_2:
        nbuses = len(voltage.keys())
        nnodes = nbuses + len(genrxtran.keys())
        ngenerators = len(generation_buses)
        Y = np.zeros((nbuses,nbuses),complex)
        for branch in branchrx:
            Y[busindex[branch[0]],busindex[branch[0]]] = Y[busindex[branch[0]],busindex[branch[0]]] + 1/branchrx[branch]
            Y[busindex[branch[1]],busindex[branch[1]]] = Y[busindex[branch[1]],busindex[branch[1]]] + 1/branchrx[branch]
            Y[busindex[branch[0]],busindex[branch[1]]] = Y[busindex[branch[0]],busindex[branch[1]]] - 1/branchrx[branch]
            Y[busindex[branch[1]],busindex[branch[0]]] = Y[busindex[branch[1]],busindex[branch[0]]] - 1/branchrx[branch]
        for branch in branchgb:
            Y[busindex[branch[0]],busindex[branch[0]]] = Y[busindex[branch[0]],busindex[branch[0]]] + branchgb[branch]/2
            Y[busindex[branch[1]],busindex[branch[1]]] = Y[busindex[branch[1]],busindex[branch[1]]] + branchgb[branch]/2
        for transf in transfrx12:
            Y[busindex[transf[0]],busindex[transf[0]]] = Y[busindex[transf[0]],busindex[transf[0]]] + 1/transfrx12[transf]
            Y[busindex[transf[1]],busindex[transf[1]]] = Y[busindex[transf[1]],busindex[transf[1]]] + 1/transfrx12[transf]
            Y[busindex[transf[0]],busindex[transf[1]]] = Y[busindex[transf[0]],busindex[transf[1]]] - 1/transfrx12[transf]
            Y[busindex[transf[1]],busindex[transf[0]]] = Y[busindex[transf[1]],busindex[transf[0]]] - 1/transfrx12[transf]
        for load in pqload:
            Y[busindex[load],busindex[load]] += np.conjugate(pqload[load]*load_factor)/sbase
        #Y[busindex[4],busindex[4]] += complex(0.0,1.64)

        # Extended admitance matrix, including:
        #  - the internal nodes in the Thevenin equivalent of the generators
        #  - the loads
        Y_ext = np.zeros((nnodes,nnodes),complex)
        Y_ext[0:nbuses,0:nbuses] = Y
        for generator in generators:
            Y_ext[gennodeindex[generator],gennodeindex[generator]] += 1/(genrxtran[generator]*sbase/genbasmva[generator])
            Y_ext[busindex[generator[0]],busindex[generator[0]]] += 1/(genrxtran[generator]*sbase/genbasmva[generator])
            Y_ext[gennodeindex[generator],busindex[generator[0]]] -= 1/(genrxtran[generator]*sbase/genbasmva[generator])
            Y_ext[busindex[generator[0]],gennodeindex[generator]] -= 1/(genrxtran[generator]*sbase/genbasmva[generator])
        #for load in pqload:
        #    Y_ext[busindex[load[0]],busindex[load[0]]] += np.conjugate(pqload[load])/sbase/abs(voltage[load[0]])**2

        fault_bus_1 = 19
        fault_branch_1 = (19,34,'1 ')

        Y_fault_ext = Y_ext.copy()
        Y_fault_ext[busindex[fault_bus_1],busindex[fault_bus_1]] += complex(0,-1e6)

        Y_fault_reduced_1 = Y_fault_ext[nbuses:nnodes,nbuses:nnodes]-np.dot(np.dot(Y_fault_ext[nbuses:nnodes,0:nbuses],np.linalg.inv(Y_fault_ext[0:nbuses,0:nbuses])),Y_fault_ext[0:nbuses,nbuses:nnodes])

        Y_postfault_ext = Y_ext.copy()
        Y_postfault_ext[busindex[fault_branch_1[0]],busindex[fault_branch_1[0]]] += - 1/branchrx[fault_branch_1]
        Y_postfault_ext[busindex[fault_branch_1[1]],busindex[fault_branch_1[1]]] += - 1/branchrx[fault_branch_1]
        Y_postfault_ext[busindex[fault_branch_1[0]],busindex[fault_branch_1[1]]] += + 1/branchrx[fault_branch_1]
        Y_postfault_ext[busindex[fault_branch_1[1]],busindex[fault_branch_1[0]]] += + 1/branchrx[fault_branch_1]
        Y_postfault_ext[busindex[fault_branch_1[0]],busindex[fault_branch_1[0]]] += - branchgb[fault_branch_1]/2
        Y_postfault_ext[busindex[fault_branch_1[1]],busindex[fault_branch_1[1]]] += - branchgb[fault_branch_1]/2

        Y_postfault_reduced_1 = Y_postfault_ext[nbuses:nnodes,nbuses:nnodes]-np.dot(np.dot(Y_postfault_ext[nbuses:nnodes,0:nbuses],np.linalg.inv(Y_postfault_ext[0:nbuses,0:nbuses])),Y_postfault_ext[0:nbuses,nbuses:nnodes])

        fault_bus_2 = 49
        fault_branch_2 = (49,54,'1 ')

        Y_fault_ext = Y_ext.copy()
        Y_fault_ext[busindex[fault_bus_2],busindex[fault_bus_2]] += complex(0,-1e6)

        Y_fault_reduced_2 = Y_fault_ext[nbuses:nnodes,nbuses:nnodes]-np.dot(np.dot(Y_fault_ext[nbuses:nnodes,0:nbuses],np.linalg.inv(Y_fault_ext[0:nbuses,0:nbuses])),Y_fault_ext[0:nbuses,nbuses:nnodes])

        Y_postfault_ext = Y_ext.copy()
        Y_postfault_ext[busindex[fault_branch_2[0]],busindex[fault_branch_2[0]]] += - 1/branchrx[fault_branch_2]
        Y_postfault_ext[busindex[fault_branch_2[1]],busindex[fault_branch_2[1]]] += - 1/branchrx[fault_branch_2]
        Y_postfault_ext[busindex[fault_branch_2[0]],busindex[fault_branch_2[1]]] += + 1/branchrx[fault_branch_2]
        Y_postfault_ext[busindex[fault_branch_2[1]],busindex[fault_branch_2[0]]] += + 1/branchrx[fault_branch_2]
        Y_postfault_ext[busindex[fault_branch_2[0]],busindex[fault_branch_2[0]]] += - branchgb[fault_branch_2]/2
        Y_postfault_ext[busindex[fault_branch_2[1]],busindex[fault_branch_2[1]]] += - branchgb[fault_branch_2]/2

        Y_postfault_reduced_2 = Y_postfault_ext[nbuses:nnodes,nbuses:nnodes]-np.dot(np.dot(Y_postfault_ext[nbuses:nnodes,0:nbuses],np.linalg.inv(Y_postfault_ext[0:nbuses,0:nbuses])),Y_postfault_ext[0:nbuses,nbuses:nnodes])

        n_gen = len(genp)
        n_branch = len(branchrx)+len(transfrx12)
#        name_gms = "tscopf_pcte_" + str(load_factor) + "_" + str(clearing_time) + ".gms"
#        name_gms = "tscopf_pcte_" + str(angle_limit) + "_" + str(sim_time) + ".gms"
        name_gms = "tscopf_pcte_fault1_" + str(clearing_time_1) + "_" + str(clearing_time_2) + ".gms"
#        name_gms = "tscopf_pcte_nodym.gms"
        f = open(name_gms,'w')

        f.write("""Scalars
        Sb "Potencia base en [MVA]" /100/""")
        f.write("\n    Dt Paso de integracion en [s] /" + str(deltat)+"/")
#        f.write("\n    angle_limit  \"etc\" /"+str(angle_limit)+"/\n\n")
        f.write("\n\n")

        f.write("Sets")
        f.write("\n    s samples /1 * "  + str(int(sim_time/deltat)) + "/")
        f.write('\n    sfirst(s) first sample')
        f.write("\n    i(s) iterations /2 * "  + str(int(sim_time/deltat)) + "/")
        f.write("\n    sf_1(s) samples_fault /1 * "  + str(int(clearing_time_1/deltat)) + "/")
        f.write("\n    spf_1(s) samples_postfault /" + str(int(clearing_time_1/deltat)+1) + " * "  + str(int(sim_time/deltat)) + "/")
        f.write("\n    sf_2(s) samples_fault /1 * "  + str(int(clearing_time_2/deltat)) + "/")
        f.write("\n    spf_2(s) samples_postfault /" + str(int(clearing_time_2/deltat)+1) + " * "  + str(int(sim_time/deltat)) + "/")
        setbusesline = "\n    b buses /"
        setgeneratorsline = "\n    g(b) generators /"
        #setgenbusesline = "    genbuses:="
        setnongenbusesline = "\n    ngb(b) nongenbuses /"
        firstbus="yes"
        firstgenerator="yes"
        firstnongenbus="yes"
        for bus in bus_name.keys():
            if firstbus=="yes":
                setbusesline += str(bus)
                firstbus="no"
            else:
                setbusesline += ", " + str(bus)
            if bus in generation_buses:
                if firstgenerator=="yes":
                    setgeneratorsline += str(bus)
                    firstgenerator="no"
                else:
                    setgeneratorsline += ", " + str(bus)
        #        setgenbusesline += " " + str(bus)
            else:
                if firstnongenbus=="yes":
                    setnongenbusesline += str(bus)
                    firstnongenbus="no"
                else:
                    setnongenbusesline += ", " + str(bus)
        setbusesline += "/"
        setgeneratorsline += "/" 
        #setgenbusesline += "/
        setnongenbusesline += "/" 
        f.write(setbusesline)
        f.write(setgeneratorsline)
        #f.write(setgenbusesline)
        f.write(setnongenbusesline)
        f.write(';\n\n')

        f.write('sfirst(s) = yes$(ord(s) eq 1);\n')
        f.write('alias (g,gp);\n')
        f.write('\n')

        f.write("Parameters")

        f.write("\n    cost_a(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), a[gen]))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), a[gen]))
        f.write('/')

        f.write("\n    cost_b(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), b[gen]))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), b[gen]))
        f.write('/')

        f.write("\n    cost_c(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), c[gen]))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), c[gen]))
        f.write('/')

        f.write("\n    Pmax(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), genpmax[gen]/sbase))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), genpmax[gen]/sbase))
        f.write('/')

        f.write("\n    Pmin(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), genpmin[gen]/sbase))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), genpmin[gen]/sbase))
        f.write('/')

        f.write("\n    Qmax(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), genqmax[gen]/sbase))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), genqmax[gen]/sbase))
        f.write('/')

        f.write("\n    Qmin(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), genqmin[gen]/sbase))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), genqmin[gen]/sbase))
        f.write('/')

        f.write("\n    e_fd_max(g) /")
        first="yes"
        for i in generation_buses:
            if first=="yes":
                f.write("%i %f" %(i, 3.0))
                first="no"
            else:
                f.write(", %i %f" %(i, 3.0))
        f.write('/\n')

        f.write("\n    e_fd_min(g) /")
        first="yes"
        for i in generation_buses:
            if first=="yes":
                f.write("%i %f" %(i, 0.0))
                first="no"
            else:
                f.write(", %i %f" %(i, 0.0))
        f.write('/\n')

        f.write("\n    Ra(g) /")
        first="yes"
        for i in generation_buses:
            if first=="yes":
                f.write("%i %f" %(i, 0.0))
                first="no"
            else:
                f.write(", %i %f" %(i, 0.0))
        f.write('/\n')

        f.write("\n    Xd(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), 1.5/genbasmva[gen]*sbase))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), 1.5/genbasmva[gen]*sbase))
        f.write('/\n')

        f.write("\n    Xd_p(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), 0.3/genbasmva[gen]*sbase))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), 0.3/genbasmva[gen]*sbase))
        f.write('/\n')

        f.write("\n    Xq(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), 1.5/genbasmva[gen]*sbase))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), 1.5/genbasmva[gen]*sbase))
        f.write('/\n')

        f.write("\n    Xq_p(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), 0.3/genbasmva[gen]*sbase))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), 0.3/genbasmva[gen]*sbase))
        f.write('/\n')

        f.write("\n    H(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), 4.5*genbasmva[gen]/sbase))
                first="no"
            else:
                if gen[0]==19:
                    f.write(", %i %f" %(float(gen[0]), 3.0*genbasmva[gen]/sbase))
                elif gen[0]==49:
                    f.write(", %i %f" %(float(gen[0]), 3.0*genbasmva[gen]/sbase))
                else:
                    f.write(", %i %f" %(float(gen[0]), 4.5*genbasmva[gen]/sbase))
        f.write('/\n')

        f.write("\n    D(g) /")
        first="yes"
        for gen in generators:
            if first=="yes":
                f.write("%i %f" %(float(gen[0]), 2.0*genbasmva[gen]/sbase))
                first="no"
            else:
                f.write(", %i %f" %(float(gen[0]), 2.0*genbasmva[gen]/sbase))
        f.write('/\n')

        f.write("\n    Td_p(g) /")
        first="yes"
        for i in generation_buses:
            if first=="yes":
                f.write("%i %f" %(i, 6.0))
                first="no"
            else:
                f.write(", %i %f" %(i, 6.0))
        f.write('/\n')

        f.write("\n    Tq_p(g) /")
        first="yes"
        for i in generation_buses:
            if first=="yes":
                f.write("%i %f" %(i, 0.5))
                first="no"
            else:
                f.write(", %i %f" %(i, 0.5))
        f.write('/\n')

        f.write("\n    K_exc(g) /")
        first="yes"
        for i in generation_buses:
            if first=="yes":
                f.write("%i %f" %(i, 100.0))
                first="no"
            else:
                f.write(", %i %f" %(i, 100.0))
        f.write('/\n')

        f.write("\n    T_exc(g) /")
        first="yes"
        for i in generation_buses:
            if first=="yes":
                f.write("%i %f" %(i, 1.0))
                first="no"
            else:
                f.write(", %i %f" %(i, 1.0))
        f.write('/\n')

        f.write("\n    K_tg(g) /")
        first="yes"
        for i in generation_buses:
            if first=="yes":
                f.write("%i %f" %(i, 50.0))
                first="no"
            else:
                f.write(", %i %f" %(i, 100.0))
        f.write('/\n')

        f.write("\n    T_tg(g) /")
        first="yes"
        for i in generation_buses:
            if first=="yes":
                f.write("%i %f" %(i, 1.0))
                first="no"
            else:
                f.write(", %i %f" %(i, 1.0))
        f.write('/\n')

#        f.write("\n    Pprog(g) /")
#        first="yes"
#        for gen in generators:
#            if first=="yes":
#                f.write("%i %f" %(float(gen[0]), genp[gen]/sbase))
#                first="no"
#            else:
#                f.write(", %i %f" %(float(gen[0]), genp[gen]/sbase))
#        f.write('/\n')

        Y_dec = "\nTable Y(b,b)\n    "
        for i in range(0,nbuses):
            Y_dec += "%10i " %(i+1)
        for i in range(0,nbuses):
            Y_dec += "\n"
            Y_dec += "%3i " %(i+1)
            for j in range(0,nbuses):
                Y_dec += "%10.5f " %np.abs(Y[i,j])
        Y_dec += ";\n"
        f.write(Y_dec)

        theta_dec = "\nTable theta(b,b)\n    "
        for i in range(0,nbuses):
            theta_dec += "%10i " %(i+1)
        for i in range(0,nbuses):
            theta_dec += "\n"
            theta_dec += "%3i " %(i+1)
            for j in range(0,nbuses):
                theta_dec += "%10.5f " %np.angle(Y[i,j])
        theta_dec += ";\n"
        f.write(theta_dec)

        Y_fdec = "\nTable Y_f_red_1(g,g)\n    "
        for generator in generators:
            Y_fdec += "%10i " %generator[0]
        for generator_row in generators:
            Y_fdec += "\n"
            Y_fdec += "%3i " %generator_row[0]
            for generator_col in generators:
                Y_fdec += "%10.5f " %np.abs(Y_fault_reduced_1[gennodeindex[generator_row]-bus_counter,gennodeindex[generator_col]-bus_counter])
        Y_fdec += ";\n"
        f.write(Y_fdec)

        theta_fdec = "\nTable theta_f_red_1(g,g)\n    "
        for generator in generators:
            theta_fdec += "%10i " %generator[0]
        for generator_row in generators:
            theta_fdec += "\n"
            theta_fdec += "%3i " %generator_row[0]
            for generator_col in generators:
                theta_fdec += "%10.5f " %np.angle(Y_fault_reduced_1[gennodeindex[generator_row]-bus_counter,gennodeindex[generator_col]-bus_counter])
        theta_fdec += ";\n"
        f.write(theta_fdec)

        Y_fdec = "\nTable Y_f_red_2(g,g)\n    "
        for generator in generators:
            Y_fdec += "%10i " %generator[0]
        for generator_row in generators:
            Y_fdec += "\n"
            Y_fdec += "%3i " %generator_row[0]
            for generator_col in generators:
                Y_fdec += "%10.5f " %np.abs(Y_fault_reduced_2[gennodeindex[generator_row]-bus_counter,gennodeindex[generator_col]-bus_counter])
        Y_fdec += ";\n"
        f.write(Y_fdec)

        theta_fdec = "\nTable theta_f_red_2(g,g)\n    "
        for generator in generators:
            theta_fdec += "%10i " %generator[0]
        for generator_row in generators:
            theta_fdec += "\n"
            theta_fdec += "%3i " %generator_row[0]
            for generator_col in generators:
                theta_fdec += "%10.5f " %np.angle(Y_fault_reduced_2[gennodeindex[generator_row]-bus_counter,gennodeindex[generator_col]-bus_counter])
        theta_fdec += ";\n"
        f.write(theta_fdec)

        Y_pfdec = "\nTable Y_pf_red_1(g,g)\n    "
        for generator in generators:
            Y_pfdec += "%10i " %generator[0]
        for generator_row in generators:
            Y_pfdec += "\n"
            Y_pfdec += "%3i " %generator_row[0]
            for generator_col in generators:
                Y_pfdec += "%10.5f " %np.abs(Y_postfault_reduced_1[gennodeindex[generator_row]-bus_counter,gennodeindex[generator_col]-bus_counter])
        Y_pfdec += ";\n"
        f.write(Y_pfdec)

        theta_pfdec = "\nTable theta_pf_red_1(g,g)\n    "
        for generator in generators:
            theta_pfdec += "%10i " %generator[0]
        for generator_row in generators:
            theta_pfdec += "\n"
            theta_pfdec += "%3i " %generator_row[0]
            for generator_col in generators:
                theta_pfdec += "%10.5f " %np.angle(Y_postfault_reduced_1[gennodeindex[generator_row]-bus_counter,gennodeindex[generator_col]-bus_counter])
        theta_pfdec += ";\n"
        f.write(theta_pfdec)

        Y_pfdec = "\nTable Y_pf_red_2(g,g)\n    "
        for generator in generators:
            Y_pfdec += "%10i " %generator[0]
        for generator_row in generators:
            Y_pfdec += "\n"
            Y_pfdec += "%3i " %generator_row[0]
            for generator_col in generators:
                Y_pfdec += "%10.5f " %np.abs(Y_postfault_reduced_2[gennodeindex[generator_row]-bus_counter,gennodeindex[generator_col]-bus_counter])
        Y_pfdec += ";\n"
        f.write(Y_pfdec)

        theta_pfdec = "\nTable theta_pf_red_2(g,g)\n    "
        for generator in generators:
            theta_pfdec += "%10i " %generator[0]
        for generator_row in generators:
            theta_pfdec += "\n"
            theta_pfdec += "%3i " %generator_row[0]
            for generator_col in generators:
                theta_pfdec += "%10.5f " %np.angle(Y_postfault_reduced_2[gennodeindex[generator_row]-bus_counter,gennodeindex[generator_col]-bus_counter])
        theta_pfdec += ";\n"
        f.write(theta_pfdec)

        f.write("\n")
        f.write("""Variables
    Pg(g)
    Qg(g)
    Ig(g)
    phi(g)
    V(b)
    alpha(b)
    ed_p_1(g,s)
    eq_p_1(g,s)
    id_1(g,s)
    iq_1(g,s)
    e_fd_1(g,s)
    delta_1(g,s)
    Domega_1(g,s)
    Pe_1(g,s)
    delta_COI_1(s)
    speed_COI_1(s)
    Vref(g)
    Vterm_1(g,s)
    DP_1(g,s)
    ed_p_2(g,s)
    eq_p_2(g,s)
    id_2(g,s)
    iq_2(g,s)
    e_fd_2(g,s)
    delta_2(g,s)
    Domega_2(g,s)
    Pe_2(g,s)
    delta_COI_2(s)
    speed_COI_2(s)
    Vref(g)
    Vterm_2(g,s)
    DP_2(g,s)
    
    z;

    Pg.l(g) = 0;
    Qg.l(g) = 0;
    Ig.l(g) = 1; Ig.lo(g) = 0.001; Ig.up(g) = Pmax(g)*1.4;
    phi.l(g) = 0; phi.lo(g) = -pi/2; phi.up(g) = pi/2;
    V.l(b) = 1; V.lo(b) = 0.98; V.up(b) = 1.5;
    alpha.l(b) = 0; alpha.lo(b) = -pi; alpha.up(b) = pi;
    ed_p_1.l(g,s) = 1; ed_p_1.lo(g,s) = 0; ed_p_1.up(g,s) = 1.5;
    eq_p_1.l(g,s) = 1; eq_p_1.lo(g,s) = 0; eq_p_1.up(g,s) = 1.5;
    id_1.l(g,s) = 1; id_1.lo(g,s) = -Pmax(g)*1.4; id_1.up(g,s) = 3*Pmax(g)*1.4;
    iq_1.l(g,s) = 1; iq_1.lo(g,s) = -Pmax(g)*1.4; iq_1.up(g,s) = 3*Pmax(g)*1.4;
    e_fd_1.l(g,s) = 1;
    delta_1.l(g,s)= 0; delta_1.lo(g,s) = -9999; delta_1.up(g,s) = 9999;
    Domega_1.l(g,s) = 0; Domega_1.lo(g,s) = -9999.9; Domega_1.up(g,s) = 9999.9;
    Pe_1.l(g,s) = 0; Pe_1.lo(g,s) = -9999; Pe_1.up(g,s) = 9999;
*    delta_COI_1.l(s) = 0; delta_COI_1.lo(s) = -9999; delta_COI_1.up(s) = 9999;
*    speed_COI_1.l(s) = 0; speed_COI_1.lo(s) = -9999; speed_COI_1.up(s) = 9999;
    delta_COI_1.l(s) = 0;
    speed_COI_1.l(s) = 0;
    Vref.l(g) = 1; Vterm_1.l(g,s) = 1;
    DP_1.l(g,s) = 0;
    ed_p_2.l(g,s) = 1; ed_p_2.lo(g,s) = 0; ed_p_2.up(g,s) = 1.5;
    eq_p_2.l(g,s) = 1; eq_p_2.lo(g,s) = 0; eq_p_2.up(g,s) = 1.5;
    id_2.l(g,s) = 1; id_2.lo(g,s) = -Pmax(g)*1.4; id_2.up(g,s) = 3*Pmax(g)*1.4;
    iq_2.l(g,s) = 1; iq_2.lo(g,s) = -Pmax(g)*1.4; iq_2.up(g,s) = 3*Pmax(g)*1.4;
    e_fd_2.l(g,s) = 1;
    delta_2.l(g,s)= 0; delta_2.lo(g,s) = -9999; delta_2.up(g,s) = 9999;
    Domega_2.l(g,s) = 0; Domega_2.lo(g,s) = -9999.9; Domega_2.up(g,s) = 9999.9;
    Pe_2.l(g,s) = 0; Pe_2.lo(g,s) = -9999; Pe_2.up(g,s) = 9999;
*    delta_COI_2.l(s) = 0; delta_COI_2.lo(s) = -9999; delta_COI_2.up(s) = 9999;
*    speed_COI_2.l(s) = 0; speed_COI_2.lo(s) = -9999; speed_COI_2.up(s) = 9999;
    delta_COI_2.l(s) = 0;
    speed_COI_2.l(s) = 0;
    Vref.l(g) = 1; Vterm_2.l(g,s) = 1;
    DP_2.l(g,s) = 0;

    Equations
    total_cost

    p_balance_gen
    p_balance_nongen
    q_balance_gen
    q_balance_nongen
    ref_bus

    P_gen_lim_inf
    P_gen_lim_sup
    Q_gen_lim_inf
    Q_gen_lim_sup

    Generators_current
    Power_factor

    e_fd_lim_inf_1
    e_fd_lim_sup_1
    e_fd_lim_inf_2
    e_fd_lim_sup_2

    ed_p_initialization_1
    eq_p_initialization_1
    Vd_initialization_1
    Vq_initialization_1
    Pe_initialization_1
    Domega_initialization_1
    id_initialization_1
    iq_initialization_1
    Vref_initialization_1
    DP_initialization_1
    
    Internal_voltaje_p_1
    Internal_voltaje_q_1
    oscilation_omega_1
    oscilation_delta_1
    excitation_system_1
    turbine_governor_1
    electric_power_fault_1
    electric_power_postfault_1
    vterm_calc_1

    id_stator_fault_1
    iq_stator_fault_1
    id_stator_postfault_1
    iq_stator_postfault_1

    center_of_inertia_1
    center_of_inertia_speed_1
*    angular_deviation_min_1
*    angular_deviation_max_1
    speed_deviation_min_1
    speed_deviation_max_1

    ed_p_initialization_2
    eq_p_initialization_2
    Vd_initialization_2
    Vq_initialization_2
    Pe_initialization_2
    Domega_initialization_2
    id_initialization_2
    iq_initialization_2
    Vref_initialization_2
    DP_initialization_2
    
    Internal_voltaje_p_2
    Internal_voltaje_q_2
    oscilation_omega_2
    oscilation_delta_2
    excitation_system_2
    turbine_governor_2
    electric_power_fault_2
    electric_power_postfault_2
    vterm_calc_2

    id_stator_fault_2
    iq_stator_fault_2
    id_stator_postfault_2
    iq_stator_postfault_2

    center_of_inertia_2
    center_of_inertia_speed_2
*    angular_deviation_min_2
*    angular_deviation_max_2;
    speed_deviation_min_2
    speed_deviation_max_2;

* Objetive function
    total_cost .. z =e= sum(g,cost_a(g)+Pg(g)*Sb*cost_b(g)+Pg(g)*Pg(g)*Sb*Sb*cost_c(g));
*    total_cost .. z =e= (sum(g,(sqr(Pg(g)-Pprog(g)))*cost(g)));
*    total_cost .. z =e= (sum(g,(Pg(g))));

* Power Flow equations
    p_balance_gen(g) ..       Pg(g) -   V(g)*sum(b,V(b)  *Y(g,b)*cos(  alpha(g) - alpha(b) -   theta(g,b))) =e= 0;
    p_balance_nongen(ngb) ..        - V(ngb)*sum(b,V(b)*Y(ngb,b)*cos(alpha(ngb) - alpha(b) - theta(ngb,b))) =e= 0;
    q_balance_gen(g) ..       Qg(g) -   V(g)*sum(b,V(b)  *Y(g,b)*sin(  alpha(g) - alpha(b) -   theta(g,b))) =e= 0;
    q_balance_nongen(ngb) ..        - V(ngb)*sum(b,V(b)*Y(ngb,b)*sin(alpha(ngb) - alpha(b) - theta(ngb,b))) =e= 0;

    ref_bus .. alpha('1') =e= 0;

* Generators limits
    P_gen_lim_inf(g) .. Pmin(g) =l= Pg(g);
    P_gen_lim_sup(g) .. Pg(g) =l= Pmax(g);
    Q_gen_lim_inf(g) .. Qmin(g) =l= Qg(g);
    Q_gen_lim_sup(g) .. Qg(g) =l= Qmax(g);

* Auxiliary equations
    Generators_current(g) .. sqr(Ig(g)*V(g)) - sqr(Pg(g)) - sqr(Qg(g)) =e= 0;
    Power_factor(g) .. sin(phi(g)) - Qg(g)/(V(g)*Ig(g)) =e=0;

* Initial condition equations
    ed_p_initialization_1(g) .. ed_p_1(g,'1') - (Xq(g) - Xq_p(g))*Ig(g)*cos(delta_1(g,'1') - alpha(g) + phi(g)) =e= 0;
    eq_p_initialization_1(g) .. eq_p_1(g,'1') + (Xd(g) - Xd_p(g))*Ig(g)*sin(delta_1(g,'1') - alpha(g) + phi(g)) - e_fd_1(g,'1') =e= 0;
    Vd_initialization_1(g) .. V(g)*sin(delta_1(g,'1') - alpha(g)) - ed_p_1(g,'1') + (Ra(g)*sin(delta_1(g,'1') - alpha(g) + phi(g))
-  Xq_p(g)*cos(delta_1(g,'1') - alpha(g) + phi(g)))*Ig(g) =e= 0;
    Vq_initialization_1(g) .. V(g)*cos(delta_1(g,'1') - alpha(g)) - eq_p_1(g,'1') + (Ra(g)*cos(delta_1(g,'1') - alpha(g) + phi(g))
+  Xd_p(g)*sin(delta_1(g,'1') - alpha(g) + phi(g)))*Ig(g) =e= 0;
    Pe_initialization_1(g) .. Pe_1(g,'1') - Pg(g) =e= 0;
    Domega_initialization_1(g) .. Domega_1(g,'1') =e= 0;
    id_initialization_1(g) .. id_1(g,'1') - Ig(g)*sin(delta_1(g,'1') - alpha(g) + phi(g)) =e= 0;
    iq_initialization_1(g) .. iq_1(g,'1') - Ig(g)*cos(delta_1(g,'1') - alpha(g) + phi(g)) =e= 0;
    Vref_initialization_1(g) .. Vref(g) - V(g) - e_fd_1(g,'1')/K_exc(g) =e= 0;
    DP_initialization_1(g) .. DP_1(g,'1') =e= 0;
    ed_p_initialization_2(g) .. ed_p_2(g,'1') - (Xq(g) - Xq_p(g))*Ig(g)*cos(delta_2(g,'1') - alpha(g) + phi(g)) =e= 0;
    eq_p_initialization_2(g) .. eq_p_2(g,'1') + (Xd(g) - Xd_p(g))*Ig(g)*sin(delta_2(g,'1') - alpha(g) + phi(g)) - e_fd_2(g,'1') =e= 0;
    Vd_initialization_2(g) .. V(g)*sin(delta_2(g,'1') - alpha(g)) - ed_p_2(g,'1') + (Ra(g)*sin(delta_2(g,'1') - alpha(g) + phi(g))
-  Xq_p(g)*cos(delta_2(g,'1') - alpha(g) + phi(g)))*Ig(g) =e= 0;
    Vq_initialization_2(g) .. V(g)*cos(delta_2(g,'1') - alpha(g)) - eq_p_2(g,'1') + (Ra(g)*cos(delta_2(g,'1') - alpha(g) + phi(g))
+  Xd_p(g)*sin(delta_2(g,'1') - alpha(g) + phi(g)))*Ig(g) =e= 0;
    Pe_initialization_2(g) .. Pe_2(g,'1') - Pg(g) =e= 0;
    Domega_initialization_2(g) .. Domega_2(g,'1') =e= 0;
    id_initialization_2(g) .. id_2(g,'1') - Ig(g)*sin(delta_2(g,'1') - alpha(g) + phi(g)) =e= 0;
    iq_initialization_2(g) .. iq_2(g,'1') - Ig(g)*cos(delta_2(g,'1') - alpha(g) + phi(g)) =e= 0;
    Vref_initialization_2(g) .. Vref(g) - V(g) - e_fd_2(g,'1')/K_exc(g) =e= 0;
    DP_initialization_2(g) .. DP_2(g,'1') =e= 0;

* Limits of variables
    e_fd_lim_inf_1(g) .. e_fd_min(g) =l= e_fd_1(g,'1');
    e_fd_lim_sup_1(g) .. e_fd_1(g,'1') =l= e_fd_max(g);
    e_fd_lim_inf_2(g) .. e_fd_min(g) =l= e_fd_2(g,'1');
    e_fd_lim_sup_2(g) .. e_fd_2(g,'1') =l= e_fd_max(g);

* Discretized equations
*   Electrical equations
    Internal_voltaje_p_1(g,s)$(not sfirst(s)) .. ed_p_1(g,s)*(1 + Dt/(2*Tq_p(g))) - ed_p_1(g,s-1)*(1 - Dt/(2*Tq_p(g))) - (Dt/(2*Tq_p(g)))*(Xq(g) - Xq_p(g))*(iq_1(g,s) + iq_1(g,s-1)) =e= 0;
    Internal_voltaje_q_1(g,s)$(not sfirst(s)) .. eq_p_1(g,s)*(1 + Dt/(2*Td_p(g))) - eq_p_1(g,s-1)*(1 - Dt/(2*Td_p(g))) - (Dt/(2*Td_p(g)))*(2*e_fd_1(g,s) - (Xd(g) - Xd_p(g))*(id_1(g,s) + id_1(g,s-1))) =e= 0;
    Internal_voltaje_p_2(g,s)$(not sfirst(s)) .. ed_p_2(g,s)*(1 + Dt/(2*Tq_p(g))) - ed_p_2(g,s-1)*(1 - Dt/(2*Tq_p(g))) - (Dt/(2*Tq_p(g)))*(Xq(g) - Xq_p(g))*(iq_2(g,s) + iq_2(g,s-1)) =e= 0;
    Internal_voltaje_q_2(g,s)$(not sfirst(s)) .. eq_p_2(g,s)*(1 + Dt/(2*Td_p(g))) - eq_p_2(g,s-1)*(1 - Dt/(2*Td_p(g))) - (Dt/(2*Td_p(g)))*(2*e_fd_2(g,s) - (Xd(g) - Xd_p(g))*(id_2(g,s) + id_2(g,s-1))) =e= 0;

*   Mechanical equations
    oscilation_omega_1(g,s)$(not sfirst(s)) .. Domega_1(g,s)*(1 + Dt*D(g)/(4*H(g))) - Domega_1(g,s-1)*(1 - Dt*D(g)/(4*H(g))) - (Dt/(4*H(g)))*(2*(Pg(g)+DP_1(g,s)) - Pe_1(g,s) - Pe_1(g,s-1)) =e= 0;
    oscilation_delta_1(g,s)$(not sfirst(s)) .. delta_1(g,s) - delta_1(g,s-1) - (Dt*100*pi/2)*(Domega_1(g,s) + Domega_1(g,s-1)) =e= 0;
    oscilation_omega_2(g,s)$(not sfirst(s)) .. Domega_2(g,s)*(1 + Dt*D(g)/(4*H(g))) - Domega_2(g,s-1)*(1 - Dt*D(g)/(4*H(g))) - (Dt/(4*H(g)))*(2*(Pg(g)+DP_2(g,s)) - Pe_2(g,s) - Pe_2(g,s-1)) =e= 0;
    oscilation_delta_2(g,s)$(not sfirst(s)) .. delta_2(g,s) - delta_2(g,s-1) - (Dt*100*pi/2)*(Domega_2(g,s) + Domega_2(g,s-1)) =e= 0;

*   excitation system
*    excitation_system_1(g,s)$(not sfirst(s)) .. e_fd_1(g,s) - e_fd_1(g,s-1) - Dt/2/T_exc(g)*(K_exc(g)*(2*Vref(g)-Vterm_1(g,s)-Vterm_1(g,s-1))-*e_fd_1(g,s)-e_fd_1(g,s-1)) =e= 0;
*    excitation_system_2(g,s)$(not sfirst(s)) .. e_fd_2(g,s) - e_fd_2(g,s-1) - Dt/2/T_exc(g)*(K_exc(g)*(2*Vref(g)-Vterm_2(g,s)-Vterm_2(g,s-1))-*e_fd_2(g,s)-e_fd_2(g,s-1)) =e= 0;
    excitation_system_1(g,s)$(not sfirst(s)) .. e_fd_1(g,s) - e_fd_1(g,s-1) =e= 0;
    excitation_system_2(g,s)$(not sfirst(s)) .. e_fd_2(g,s) - e_fd_2(g,s-1) =e= 0;

*   turbine governor
*    turbine_governor_1(g,s)$(not sfirst(s)) .. DP_1(g,s) - DP_1(g,s-1) - Dt/2/T_tg(g)*(K_tg(g)*(-Domega_1(g,s)-Domega_1(g,s-1))-DP_1(g,s)-DP_1(g,s-1)) =e= 0;
*    turbine_governor_2(g,s)$(not sfirst(s)) .. DP_2(g,s) - DP_2(g,s-1) - Dt/2/T_tg(g)*(K_tg(g)*(-Domega_2(g,s)-Domega_2(g,s-1))-DP_2(g,s)-DP_2(g,s-1)) =e= 0;
    turbine_governor_1(g,s)$(not sfirst(s)) .. DP_1(g,s) - DP_1(g,s-1) =e= 0;
    turbine_governor_2(g,s)$(not sfirst(s)) .. DP_2(g,s) - DP_2(g,s-1) =e= 0;

*   Electrical power output equations
    electric_power_fault_1(g,sf_1)$(not sfirst(sf_1)) .. Pe_1(g,sf_1) - ed_p_1(g,sf_1)*id_1(g,sf_1) - eq_p_1(g,sf_1)*iq_1(g,sf_1) =e= 0;
    electric_power_postfault_1(g,spf_1) .. Pe_1(g,spf_1) - ed_p_1(g,spf_1)*id_1(g,spf_1) - eq_p_1(g,spf_1)*iq_1(g,spf_1) =e= 0;
    electric_power_fault_2(g,sf_2)$(not sfirst(sf_2)) .. Pe_2(g,sf_2) - ed_p_2(g,sf_2)*id_2(g,sf_2) - eq_p_2(g,sf_2)*iq_2(g,sf_2) =e= 0;
    electric_power_postfault_2(g,spf_2) .. Pe_2(g,spf_2) - ed_p_2(g,spf_2)*id_2(g,spf_2) - eq_p_2(g,spf_2)*iq_2(g,spf_2) =e= 0;

*   Vterm
    vterm_calc_1(g,s) .. Vterm_1(g,s) - sqrt( sqr(ed_p_1(g,s)+Xd_p(g)*iq_1(g,s)) + sqr(eq_p_1(g,s)-Xd_p(g)*id_1(g,s)) ) =e= 0;
    vterm_calc_2(g,s) .. Vterm_2(g,s) - sqrt( sqr(ed_p_2(g,s)+Xd_p(g)*iq_2(g,s)) + sqr(eq_p_2(g,s)-Xd_p(g)*id_2(g,s)) ) =e= 0;

*   dq current equations
    id_stator_fault_1(g,sf_1)$(not sfirst(sf_1)) .. id_1(g,sf_1) - sum(gp,Y_f_red_1(g,gp)*(ed_p_1(gp,sf_1)*cos(delta_1(g,sf_1) - delta_1(gp,sf_1) - theta_f_red_1(g,gp)) + eq_p_1(gp,sf_1)*sin(delta_1(g,sf_1) - delta_1(gp,sf_1) - theta_f_red_1(g,gp)))) =e= 0;
    iq_stator_fault_1(g,sf_1)$(not sfirst(sf_1)) .. iq_1(g,sf_1) - sum(gp,Y_f_red_1(g,gp)*(eq_p_1(gp,sf_1)*cos(delta_1(g,sf_1) - delta_1(gp,sf_1) - theta_f_red_1(g,gp)) - ed_p_1(gp,sf_1)*sin(delta_1(g,sf_1) - delta_1(gp,sf_1) - theta_f_red_1(g,gp)))) =e= 0;
    id_stator_fault_2(g,sf_2)$(not sfirst(sf_2)) .. id_2(g,sf_2) - sum(gp,Y_f_red_2(g,gp)*(ed_p_2(gp,sf_2)*cos(delta_2(g,sf_2) - delta_2(gp,sf_2) - theta_f_red_2(g,gp)) + eq_p_2(gp,sf_2)*sin(delta_2(g,sf_2) - delta_2(gp,sf_2) - theta_f_red_2(g,gp)))) =e= 0;
    iq_stator_fault_2(g,sf_2)$(not sfirst(sf_2)) .. iq_2(g,sf_2) - sum(gp,Y_f_red_2(g,gp)*(eq_p_2(gp,sf_2)*cos(delta_2(g,sf_2) - delta_2(gp,sf_2) - theta_f_red_2(g,gp)) - ed_p_2(gp,sf_2)*sin(delta_2(g,sf_2) - delta_2(gp,sf_2) - theta_f_red_2(g,gp)))) =e= 0;
    id_stator_postfault_1(g,spf_1) .. id_1(g,spf_1) - sum(gp,Y_pf_red_1(g,gp)*(ed_p_1(gp,spf_1)*cos(delta_1(g,spf_1) - delta_1(gp,spf_1) - theta_pf_red_1(g,gp)) + eq_p_1(gp,spf_1)*sin(delta_1(g,spf_1) - delta_1(gp,spf_1) - theta_pf_red_1(g,gp)))) =e= 0;
    iq_stator_postfault_1(g,spf_1) .. iq_1(g,spf_1) - sum(gp,Y_pf_red_1(g,gp)*(eq_p_1(gp,spf_1)*cos(delta_1(g,spf_1) - delta_1(gp,spf_1) - theta_pf_red_1(g,gp)) - ed_p_1(gp,spf_1)*sin(delta_1(g,spf_1) - delta_1(gp,spf_1) - theta_pf_red_1(g,gp)))) =e= 0;
    id_stator_postfault_2(g,spf_2) .. id_2(g,spf_2) - sum(gp,Y_pf_red_2(g,gp)*(ed_p_2(gp,spf_2)*cos(delta_2(g,spf_2) - delta_2(gp,spf_2) - theta_pf_red_2(g,gp)) + eq_p_2(gp,spf_2)*sin(delta_2(g,spf_2) - delta_2(gp,spf_2) - theta_pf_red_2(g,gp)))) =e= 0;
    iq_stator_postfault_2(g,spf_2) .. iq_2(g,spf_2) - sum(gp,Y_pf_red_2(g,gp)*(eq_p_2(gp,spf_2)*cos(delta_2(g,spf_2) - delta_2(gp,spf_2) - theta_pf_red_2(g,gp)) - ed_p_2(gp,spf_2)*sin(delta_2(g,spf_2) - delta_2(gp,spf_2) - theta_pf_red_2(g,gp)))) =e= 0;

*   Stability criterion equations
    center_of_inertia_1(s) .. delta_COI_1(s) - sum(g,H(g)*delta_1(g,s)) / sum(g,H(g)) =e= 0;
    center_of_inertia_speed_1(s) .. speed_COI_1(s) - sum(g,H(g)*Domega_1(g,s)) / sum(g,H(g)) =e= 0;
*    angular_deviation_min_1(g,s) .. - (angle_limit*pi/180) =l= delta_1(g,s) - delta_COI_1(s);
*    angular_deviation_max_1(g,s) .. delta_1(g,s) - delta_COI_1(s) =l= (angle_limit*pi/180);
    speed_deviation_min_1(g,s) .. - .02 =l= Domega_1(g,s) - speed_COI_1(s);
    speed_deviation_max_1(g,s) .. Domega_1(g,s) - speed_COI_1(s) =l= .02;
    center_of_inertia_2(s) .. delta_COI_2(s) - sum(g,H(g)*delta_2(g,s)) / sum(g,H(g)) =e= 0;
    center_of_inertia_speed_2(s) .. speed_COI_2(s) - sum(g,H(g)*Domega_2(g,s)) / sum(g,H(g)) =e= 0;
*    angular_deviation_min_2(g,s) .. - (angle_limit*pi/180) =l= delta_2(g,s) - delta_COI_2(s);
*    angular_deviation_max_2(g,s) .. delta_2(g,s) - delta_COI_2(s) =l= (angle_limit*pi/180);
    speed_deviation_min_2(g,s) .. - .02 =l= Domega_2(g,s) - speed_COI_2(s);
    speed_deviation_max_2(g,s) .. Domega_2(g,s) - speed_COI_2(s) =l= .02;

Model tscopf /total_cost, p_balance_gen, p_balance_nongen, q_balance_gen, q_balance_nongen, ref_bus,
			  P_gen_lim_inf, P_gen_lim_sup, Q_gen_lim_inf, Q_gen_lim_sup,
			  Generators_current, Power_factor,
			  ed_p_initialization_1, eq_p_initialization_1, Vd_initialization_1, Vq_initialization_1, Pe_initialization_1,
			  Domega_initialization_1, id_initialization_1, iq_initialization_1, Vref_initialization_1, DP_initialization_1,
			  e_fd_lim_inf_1, e_fd_lim_sup_1,
			  Internal_voltaje_p_1, Internal_voltaje_q_1, oscilation_omega_1, oscilation_delta_1, excitation_system_1, turbine_governor_1,
			  electric_power_fault_1, Vterm_calc_1, id_stator_fault_1, iq_stator_fault_1,
			  electric_power_postfault_1, id_stator_postfault_1, iq_stator_postfault_1,
*			  center_of_inertia_1,
			  center_of_inertia_speed_1,
*              angular_deviation_min_1, angular_deviation_max,
              speed_deviation_min_1, speed_deviation_max_1/;
*			  ed_p_initialization_2, eq_p_initialization_2, Vd_initialization_2, Vq_initialization_2, Pe_initialization_2,
*			  Domega_initialization_2, id_initialization_2, iq_initialization_2, Vref_initialization_2, DP_initialization_2,
*			  e_fd_lim_inf_2, e_fd_lim_sup_2,
*			  Internal_voltaje_p_2, Internal_voltaje_q_2, oscilation_omega_2, oscilation_delta_2, excitation_system_2, turbine_governor_2,
*			  electric_power_fault_2, Vterm_calc_2, id_stator_fault_2, iq_stator_fault_2,
*			  electric_power_postfault_2, id_stator_postfault_2, iq_stator_postfault_2,
**			  center_of_inertia_2,
*			  center_of_inertia_speed_2,
**              angular_deviation_min_2 angular_deviation_max_2,
*              speed_deviation_min_2 speed_deviation_max_2/;
*Model tscopf /all/;

Option NLP = IPOPT;
Option Reslim = 4000;
Solve tscopf using NLP minimizing z;

Display Pg.l
Display Qg.l
Display V.l
Display alpha.l

Display delta_1.l
Display delta_2.l

file salida /plot_delta.m/;
salida.nd = 6;
put salida

put 'V = [...'/
loop(b, put V.l(b);
put ';'/);
put'];'/

put 'Pg = [...'/
loop(g, put Pg.l(g),';' /)
put'];'/

put 't = [...'/
loop(s, put (ord(s)*Dt),';' /)
put'];'/

put 'delta_1 = [...'/
loop(s,
    loop(g, put delta_1.l(g,s));
    put ';'/);
put'];'/

put 'Domega_1 = [...'/
loop(s,
    loop(g, put Domega_1.l(g,s));
    put ';'/);
put'];'/

put 'delta_COI_1 = [...'/
loop(s, put delta_COI_1.l(s),';' /)
put'];'/

put 'speed_COI_1 = [...'/
loop(s, put speed_COI_1.l(s),';' /)
put'];'/

put 'figure(1)' /
put '#plot(t,delta_1*180/pi,t,delta_COI_1*180/pi,t,delta_COI_1*180/pi + 50,t,delta_COI_1*180/pi - 50);' /
put 'plot(t,Domega_1,t,speed_COI_1,t,speed_COI_1 + 0.02,t,speed_COI_1 - 0.02);' /

put 'delta_2 = [...'/
loop(s,
    loop(g, put delta_2.l(g,s));
    put ';'/);
put'];'/

put 'Domega_2 = [...'/
loop(s,
    loop(g, put Domega_2.l(g,s));
    put ';'/);
put'];'/

put 'delta_COI_2 = [...'/
loop(s, put delta_COI_2.l(s),';' /)
put'];'/

put 'speed_COI_2 = [...'/
loop(s, put speed_COI_2.l(s),';' /)
put'];'/

put 'figure(2)' /
put '#plot(t,delta_2*180/pi,t,delta_COI_2*180/pi,t,delta_COI_2*180/pi + 50,t,delta_COI_2*180/pi - 50);' /
put 'plot(t,Domega_2,t,speed_COI_2,t,speed_COI_2 + 0.02,t,speed_COI_2 - 0.02);' /

put '%figure(1)' /
put '%bar(V);' /
put '%figure(2)' /
put '%bar(Pg);' /""")

        f.close()

