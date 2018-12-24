import string
import numpy as np
import pdb

time = 10
clearing_time = 0.3
deltat = 0.02

rawfile = open('mallorca.raw','r')
line = rawfile.readline()
if '/' in line: line = line[:line.find('/')]
words = line.split(',')
sbase = float(words[1])
comments = [rawfile.readline(),rawfile.readline()]
#sections = ('bus','load','shunt','generator','branch','transformer')

node_counter = 0
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

pqload={};pload={};qload={};
while 1:
    line = rawfile.readline()
    if '/' in line: line = line[:line.find('/')]
    words = line.split(',')
    if len(words) == 1 and int(words[0]) == 0: break
    busnumber = int(words[0])
    busid = words[1][1:-1]
    p = float(words[5])
    q = float(words[6])
    pqload[(busnumber,busid)] = complex(p,q)
    pload[busnumber] = p
    qload[busnumber] = q

while 1:
    line = rawfile.readline()
    if '/' in line: line = line[:line.find('/')]
    words = line.split(',')
    if len(words) == 1 and int(words[0]) == 0: break

genp={}; genq={}; genbasmva={}; genrxtran={}; gennodeindex={}; generation_buses=[]
genqmax={}; genqmin={}; genpmax={}; genpmin={};
while 1:
    line = rawfile.readline()
    if '/' in line: line = line[:line.find('/')]
    words = line.split(',')
    if len(words) == 1 and int(words[0]) == 0: break
    busnumber = int(words[0])
    genid = words[1][1:-1]
    genp[(busnumber,genid)] = float(words[2])
    genq[(busnumber,genid)] = float(words[3])
    genqmax[(busnumber,genid)] = float(words[4])
    genqmin[(busnumber,genid)] = float(words[5])
    genbasmva[(busnumber,genid)] = float(words[8])
    genrxtran[(busnumber,genid)] = complex(float(words[9]),float(words[10]))
    genpmax[(busnumber,genid)] = float(words[16])
    genpmin[(busnumber,genid)] = float(words[17])
    gennodeindex[(busnumber,genid)] = node_counter
    node_counter = node_counter + 1
    generation_buses.append(busnumber)

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
    while len(words) < 36: 
        next_line = rawfile.readline()
        words.extend(next_line.split(','))
    busnumber1 = int(words[0])
    busnumber2 = int(words[1])
    busnumber3 = int(words[2])
    transfid = words[3][1:-1]
    transfrx12[(busnumber1,busnumber2,busnumber2,transfid)] = complex(float(words[14]),float(words[15]))

rawfile.close()

load_factors = (.40,.45,.50,.55,.60,.65,.70,.75,.80,.85,.90,.95,1.00,1.05,1.10,1.15,1.20,1.25,1.30,1.35,1.40,1.45,1.50,1.55,1.60,1.65,1.70,1.75,1.80)
angle_limits = (60,)
for load_factor in load_factors:
    for angle_limit in angle_limits:
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
            Y[busindex[load[0]],busindex[load[0]]] += np.conjugate(pqload[load]*load_factor)/sbase
        Y[busindex[6],busindex[6]] += complex(0.0,1.23)

        # Extended admitance matrix, including:
        #  - the internal nodes in the Thevenin equivalent of the generators
        #  - the loads
        Y_ext = np.zeros((nnodes,nnodes),complex)
        Y_ext[0:nbuses,0:nbuses] = Y
        for generator in genrxtran:
            Y_ext[gennodeindex[generator],gennodeindex[generator]] += 1/(genrxtran[generator]*sbase/genbasmva[generator])
            Y_ext[busindex[generator[0]],busindex[generator[0]]] += 1/(genrxtran[generator]*sbase/genbasmva[generator])
            Y_ext[gennodeindex[generator],busindex[generator[0]]] -= 1/(genrxtran[generator]*sbase/genbasmva[generator])
            Y_ext[busindex[generator[0]],gennodeindex[generator]] -= 1/(genrxtran[generator]*sbase/genbasmva[generator])

        fault_bus = 10

        Y_fault_ext = Y_ext.copy()
        Y_fault_ext[busindex[fault_bus],busindex[fault_bus]] += complex(0,-1e6)

        #Y_fault_reduced = Y_fault_ext[nbuses:nnodes,nbuses:nnodes]-np.dot(np.dot(Y_fault_ext[nbuses:nnodes,0:nbuses],np.linalg.inv(Y_fault_ext[0:nbuses,0:nbuses])),Y_fault_ext[0:nbuses,nbuses:nnodes])
        Y_fault_ext[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]] = Y_fault_ext[:,[20,21,22,23,24,5,0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19]]
        Y_fault_ext[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],:] = Y_fault_ext[[20,21,22,23,24,5,0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19],:]
        Y_fault_reduced = Y_fault_ext[0:6,0:6]-np.dot(np.dot(Y_fault_ext[0:6,6:25],np.linalg.inv(Y_fault_ext[6:25,6:25])),Y_fault_ext[6:25,0:6])

        fault_branch = (7,10,'1 ')
        
        Y_postfault_ext = Y_ext.copy()
        Y_postfault_ext[busindex[fault_branch[0]],busindex[fault_branch[0]]] += - 1/branchrx[fault_branch]
        Y_postfault_ext[busindex[fault_branch[1]],busindex[fault_branch[1]]] += - 1/branchrx[fault_branch]
        Y_postfault_ext[busindex[fault_branch[0]],busindex[fault_branch[1]]] += + 1/branchrx[fault_branch]
        Y_postfault_ext[busindex[fault_branch[1]],busindex[fault_branch[0]]] += + 1/branchrx[fault_branch]
        Y_postfault_ext[busindex[fault_branch[0]],busindex[fault_branch[0]]] += - branchgb[fault_branch]/2
        Y_postfault_ext[busindex[fault_branch[1]],busindex[fault_branch[1]]] += - branchgb[fault_branch]/2

        #Y_postfault_reduced = Y_postfault_ext[nbuses:nnodes,nbuses:nnodes]-np.dot(np.dot(Y_postfault_ext[nbuses:nnodes,0:nbuses],np.linalg.inv(Y_postfault_ext[0:nbuses,0:nbuses])),Y_postfault_ext[0:nbuses,nbuses:nnodes])
        Y_postfault_ext[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]] = Y_postfault_ext[:,[20,21,22,23,24,5,0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19]]
        Y_postfault_ext[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],:] = Y_postfault_ext[[20,21,22,23,24,5,0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19],:]
        Y_postfault_reduced = Y_postfault_ext[0:6,0:6]-np.dot(np.dot(Y_postfault_ext[0:6,6:25],np.linalg.inv(Y_postfault_ext[6:25,6:25])),Y_postfault_ext[6:25,0:6])
        
        n_gen = len(genp)
        n_branch = len(branchrx)+len(transfrx12)
        name_gms = "calle_tscopf_pcte_" + str(angle_limit) + "_" + str(load_factor) + ".gms"
        f = open(name_gms,'w')

        f.write("""Scalars
         Sb "Potencia base en [MVA]" /100/
         Dt "Paso de integracion en [s]" /0.020000/""")
        f.write("\n         angle_limit /" + str(angle_limit) + "/\n")
        f.write("""
     
Sets
    s samples /1 * 200/
    sfirst(s) first sample
    sf(s) samples_fault /1 * 15/
    spf(s) samples_postfault /16 * 200/
    spf_1(s) samples_postfault_1 /16 * 25/
    spf_2(s) samples_postfault_2 /26 * 75/
    spf_3(s) samples_postfault_3 /76 * 200/
    b buses /1 * 20/
    rb(b) retained buses /1 * 6/
    g(rb) generators /1 * 5/
    hv(rb) buses with a fixed input power /6/
    ngb(b) nongenbuses /7 * 20/;

sfirst(s) = yes$(ord(s) eq 1);
alias (g,gp);
alias (hv,hvp);

Parameters
    a1(b) /1 7.0e1, 2 8.0e1, 3 4.00e1, 4 1.00e2, 5 1.20e2, 6 5.50e1/
    Pl(b) /1 0, 2 0, 3 0, 4 0, 5 0, 6 0, 7 0, 8 0, 9 0, 10 0, 11 0, 12 0, 13 0, 14 0, 15 0, 16 0, 17 0, 18 0, 19 0, 20 0/
    Ql(b) /1 0, 2 0, 3 0, 4 0, 5 0, 6 0, 7 0, 8 0, 9 0, 10 0, 11 0, 12 0, 13 0, 14 0, 15 0, 16 0, 17 0, 18 0, 19 0, 20 0/
    Pmax(g) /1 600, 2 470, 3 510, 4 275, 5 350/
    Pmax(g);
    Pmax(g) = pmax(g)/Sb;
Parameters
    Pmin(g) /1 0.000000, 2 0.000000, 3 0.000000, 4 0.000000, 5 0.000000/
    Qmax(g);
    Qmax(g) = Pmax(g)*0.5;
Parameters
    Qmin(g);
    Qmin(g) = -Qmax(g);
Parameters
    Sm(g);
    Sm(g) = Pmax(g)*1.1;
Parameters
    e_fd_max(g) /1 2.0, 2 2.0, 3 2.0, 4 2.0, 5 2.0/
    e_fd_min(g) /1 0.0, 2 0.0, 3 0.0, 4 0.0, 5 0.0/
    Ra(g) /1 0.0, 2 0.0, 3 0.0, 4 0.0, 5 0.0/
    Ra(g);
    Ra(g) = ra(g)/Sm(g);
Parameters
    Xd(g) /1 1.5, 2 1.5, 3 1.5, 4 1.5, 5 1.5/
    Xd(g);
    Xd(g) = xd(g)/Sm(g);
Parameters
    Xd_p(g) /1 0.3, 2 0.3, 3 0.3, 4 0.3, 5 0.3/
    Xd_p(g);
    Xd_p(g) = xd_p(g)/Sm(g);
Parameters
    Xq(g) /1 1.5, 2 1.5, 3 1.5, 4 1.5, 5 1.5/
    Xq(g);
    Xq(g) = xq(g)/Sm(g);
Parameters
    Xq_p(g) /1 0.3, 2 0.3, 3 0.3, 4 0.3, 5 0.3/
    Xq_p(g);
    Xq_p(g) = xq_p(g)/Sm(g);
Parameters
    H(g) /1 3.2, 2 3.0, 3 3.0, 4 2.0, 5 2.0/
    H(g);
    H(g) = h(g)*Sm(g);
Parameters
    D(g) /1 2.0, 2 2.0, 3 2.0, 4 2.0, 5 2.0/
    D(g);
    D(g) = d(g)*Sm(g);
Parameters
    Td_p(g) /1 6.0, 2 6.0, 3 6.0, 4 6.0, 5 6.0/
    Tq_p(g) /1 1.0, 2 1.0, 3 1.0, 4 1.0, 5 1.0/;\n""")

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

        Y_fdec = "\nTable Y_f_red(rb,rb)\n    "
        for i in range(0,6):
            Y_fdec += "%10i " %(i+1)
        for i in range(0,6):
            Y_fdec += "\n"
            Y_fdec += "%3i " %(i+1)
            for j in range(0,6):
                Y_fdec += "%10.5f " %np.abs(Y_fault_reduced[i,j])
        Y_fdec += ";\n"
        f.write(Y_fdec)

        theta_fdec = "\nTable theta_f_red(rb,rb)\n    "
        for i in range(0,6):
            theta_fdec += "%10i " %(i+1)
        for i in range(0,6):
            theta_fdec += "\n"
            theta_fdec += "%3i " %(i+1)
            for j in range(0,6):
                theta_fdec += "%10.5f " %np.angle(Y_fault_reduced[i,j])
        theta_fdec += ";\n"
        f.write(theta_fdec)

        Y_pfdec = "\nTable Y_pf_red(rb,rb)\n    "
        for i in range(0,6):
            Y_pfdec += "%10i " %(i+1)
        for i in range(0,6):
            Y_pfdec += "\n"
            Y_pfdec += "%3i " %(i+1)
            for j in range(0,6):
                Y_pfdec += "%10.5f " %np.abs(Y_postfault_reduced[i,j])
        Y_pfdec += ";\n"
        f.write(Y_pfdec)

        theta_pfdec = "\nTable theta_pf_red(rb,rb)\n    "
        for i in range(0,6):
            theta_pfdec += "%10i " %(i+1)
        for i in range(0,6):
            theta_pfdec += "\n"
            theta_pfdec += "%3i " %(i+1)
            for j in range(0,6):
                theta_pfdec += "%10.5f " %np.angle(Y_postfault_reduced[i,j])
        theta_pfdec += ";\n"
        f.write(theta_pfdec)

        str_loadfactor = str(load_factor)
        str_loadfactor.split('.')

        f.write("\n")
        f.write("""Variables
        Pg(g)
        Qg(g)
        Phvdc(hv)
        Qhvdc(hv)
        Ig(g)
        phi(g)
        V(b)
        alpha(b)
        ed_p(g,s)
        eq_p(g,s)
        id(g,s)
        iq(g,s)
        e_fd(g)
        delta_COI(s)
        delta(g,s)
        Domega(g,s)
        Pe(g,s)
        Phvdc_1(hv,s)
        Qhvdc_1(hv,s)
        Vhvdc(hv,s)
        alpha_hvdc(hv,s)
        z;

        Pg.l('1') = 3; Pg.l('2') = 1; Pg.l('3') = 3; Pg.l('4') = 0.5; Pg.l('5') = 0.5;
        Qg.l(g) = 0;
        Phvdc.l(hv) = 3.0; Phvdc.lo(hv) = 0.0;    Phvdc.up(hv) = 3.10;
        Qhvdc.l(hv) = -1.5; Qhvdc.lo(hv) = -1.55; Qhvdc.up(hv) = 0.0;
        Ig.l(g) = 1; Ig.lo(g) = 0.001; Ig.up(g) = Sm(g);
        phi.l(g) = 0; phi.lo(g) = -pi/2; phi.up(g) = pi/2;
        V.l(b) = 0.95; V.lo(b) = 0.95; V.up(b) = 1.05;
        alpha.l(b) = 0; alpha.lo(b) = -pi; alpha.up(b) = pi;
        ed_p.l(g,s) = 0.2; ed_p.lo(g,s) = 0; ed_p.up(g,s) = 1.5;
        eq_p.l(g,s) = 1.0; eq_p.lo(g,s) = 0; eq_p.up(g,s) = 1.5;
        id.l(g,s) = 1; id.lo(g,s) = -Sm(g); id.up(g,s) = 3*Sm(g);
        iq.l(g,s) = 1; iq.lo(g,s) = -Sm(g); iq.up(g,s) = 3*Sm(g);
        e_fd.l(g) = 1;
        delta_COI.l(s) = 0; delta_COI.lo(s) = -9999; delta_COI.up(s) = 9999;
        delta.l(g,s)= 0; delta.lo(g,s) = -9999; delta.up(g,s) = 9999;
        Domega.l(g,s) = 0; Domega.lo(g,s) = -1; Domega.up(g,s) = 1;
        Pe.l(g,s) = 3.0; Pe.lo(g,s) = -99; Pe.up(g,s) = 99;
        Phvdc_1.l(hv,s) = 3.0; Phvdc_1.lo(hv,s) = 0.0; Phvdc_1.up(hv,s) = 3.10;
        Qhvdc_1.l(hv,s) = -1.5; Qhvdc_1.lo(hv,s) = -1.55; Qhvdc_1.up(hv,s) = 0.0;
        Vhvdc.l(hv,s) = 0.9; Vhvdc.lo(hv,sf) = 0.2; Vhvdc.lo(hv,spf) = 0.7; Vhvdc.up(hv,s) = 1.05;
        alpha_hvdc.l(hv,s) = 0; alpha_hvdc.lo(hv,s) = -9999; alpha_hvdc.up(hv,s) = 9999;

Equations
        total_cost

        p_balance_gen
        p_balance_HVDC
        p_balance_nongen
        q_balance_gen
        q_balance_HVDC
        q_balance_nongen
        PQ_HVDC_relation
        ref_bus

        P_gen_lim_inf
        P_gen_lim_sup
        Q_gen_lim_inf
        Q_gen_lim_sup
*       Field_current_heating_limit

        I_brach_lim_inf_1
        I_brach_lim_inf_2
        I_brach_lim_sup_1
        I_brach_lim_sup_2

        Generators_current
        Power_factor

        ed_p_initialization
        eq_p_initialization
        Vd_initialization
        Vq_initialization
        Pe_initialization
*        P_inyected_at_HVDC_bus
        Domega_initialization
        id_initialization
        iq_initialization

        e_fd_lim_inf
        e_fd_lim_sup

        Internal_voltaje_d
        Internal_voltaje_q
        oscilation_omega
        oscilation_delta
        electric_power_fault
        electric_power_postfault

        P_balanced_1_at_HVDC_bus
        Q_balanced_1_at_HVDC_bus
        P_balanced_2_at_HVDC_bus
        Q_balanced_2_at_HVDC_bus

        Q_absorbed_at_HVDC_bus
        P_inyected_1_at_HVDC_bus
        P_inyected_2_at_HVDC_bus
        P_inyected_3_at_HVDC_bus
        P_inyected_4_at_HVDC_bus

        id_stator_fault
        iq_stator_fault
        id_stator_postfault_1
        iq_stator_postfault_1

        center_of_inertia
        angular_deviation_min
        angular_deviation_max;

* Objetive function
        total_cost .. z =e= (sum(g,a1(g)*(Pg(g)*100)) + sum(hv,a1(hv)*(Phvdc(hv)*100)));

* Power Flow equations
        p_balance_gen(g) .. Pg(g) - Pl(g) - V(g)*sum(b,V(b)*Y(g,b)*cos(alpha(g) - alpha(b) - theta(g,b))) =e= 0;
        p_balance_HVDC(hv) .. Phvdc(hv) - Pl(hv) - V(hv)*sum(b,V(b)*Y(hv,b)*cos(alpha(hv) - alpha(b) - theta(hv,b))) =e= 0;
        p_balance_nongen(ngb) ..  - Pl(ngb) - V(ngb)*sum(b,V(b)*Y(ngb,b)*cos(alpha(ngb) - alpha(b) - theta(ngb,b))) =e= 0;
        q_balance_gen(g) .. Qg(g) - Ql(g) - V(g)*sum(b,V(b)*Y(g,b)*sin(alpha(g) - alpha(b) - theta(g,b))) =e= 0;
        q_balance_HVDC(hv) .. Qhvdc(hv) - Ql(hv) - V(hv)*sum(b,V(b)*Y(hv,b)*sin(alpha(hv) - alpha(b) - theta(hv,b))) =e= 0;
        q_balance_nongen(ngb) ..  - Ql(ngb) - V(ngb)*sum(b,V(b)*Y(ngb,b)*sin(alpha(ngb) - alpha(b) - theta(ngb,b))) =e= 0;

        PQ_HVDC_relation(hv) .. Qhvdc(hv) + Phvdc(hv)/2 =e= 0;

        ref_bus .. alpha('1') =e= 0;

* Generators limits
        P_gen_lim_inf(g) .. Pmin(g) =l= Pg(g);
        P_gen_lim_sup(g) .. Pg(g) =l= Pmax(g);
        Q_gen_lim_inf(g) .. Qmin(g) =l= Qg(g);
        Q_gen_lim_sup(g) .. Qg(g) =l= Qmax(g);

*       Field_current_heating_limit ..

* Current limits for the braches
*        I_brach_lim_inf(r) .. 0 =l= (sqr(V(From(r))*cos(alpha(From(r))) - V(To(r))*cos(alpha(To(r)))) + sqr(V(From(r))*sin(alpha(From(r))) - V(To(r))*sin(alpha(To(r)))))*sqr(Y(From(r),To(r)));
*        I_brach_lim_sup(r) .. (sqr(V(From(r))*cos(alpha(From(r))) - V(To(r))*cos(alpha(To(r)))) + sqr(V(From(r))*sin(alpha(From(r))) - V(To(r))*sin(alpha(To(r)))))*sqr(Y(From(r),To(r))) =l= sqr(Imx(r));
        I_brach_lim_inf_1('1') .. 0 =l= (sqr(V('13')*cos(alpha('13')) - V('14')*cos(alpha('14'))) + sqr(V('13')*sin(alpha('13')) - V('14')*sin(alpha('14'))))*sqr(Y('13','14'));
        I_brach_lim_inf_2('1') .. 0 =l= (sqr(V('15')*cos(alpha('15')) - V('16')*cos(alpha('16'))) + sqr(V('15')*sin(alpha('15')) - V('16')*sin(alpha('16'))))*sqr(Y('15','16'));
        I_brach_lim_sup_1('1') .. (sqr(V('13')*cos(alpha('13')) - V('14')*cos(alpha('14'))) + sqr(V('13')*sin(alpha('13')) - V('14')*sin(alpha('14'))))*sqr(Y('13','14')) =l= sqr(2.0);
        I_brach_lim_sup_2('1') .. (sqr(V('15')*cos(alpha('15')) - V('16')*cos(alpha('16'))) + sqr(V('15')*sin(alpha('15')) - V('16')*sin(alpha('16'))))*sqr(Y('15','16')) =l= sqr(1.8);

* Auxiliary equations
        Generators_current(g) .. sqr(Ig(g)*V(g)) - sqr(Pg(g)) - sqr(Qg(g)) =e= 0;
        Power_factor(g) .. sin(phi(g)) - Qg(g)/(V(g)*Ig(g)) =e=0;

* Initial condition equations
        ed_p_initialization(g) .. ed_p(g,'1') - (Xq(g) - Xq_p(g))*Ig(g)*cos(delta(g,'1') - alpha(g) + phi(g)) =e= 0;
        eq_p_initialization(g) .. eq_p(g,'1') + (Xd(g) - Xd_p(g))*Ig(g)*sin(delta(g,'1') - alpha(g) + phi(g)) - e_fd(g) =e= 0;
        Vd_initialization(g) .. V(g)*sin(delta(g,'1') - alpha(g)) - ed_p(g,'1') + (Ra(g)*sin(delta(g,'1') - alpha(g) + phi(g))
                                                                              -  Xq_p(g)*cos(delta(g,'1') - alpha(g) + phi(g)))*Ig(g) =e= 0;
        Vq_initialization(g) .. V(g)*cos(delta(g,'1') - alpha(g)) - eq_p(g,'1') + (Ra(g)*cos(delta(g,'1') - alpha(g) + phi(g))
                                                                              +  Xd_p(g)*sin(delta(g,'1') - alpha(g) + phi(g)))*Ig(g) =e= 0;
        Pe_initialization(g) .. Pe(g,'1') - Pg(g) =e= 0;
*        P_inyected_at_HVDC_bus(hv) .. Phvdc_1(hv,'1') - Phvdc(hv) =e= 0;
        Domega_initialization(g) .. Domega(g,'1') =e= 0;
        id_initialization(g) .. id(g,'1') - Ig(g)*sin(delta(g,'1') - alpha(g) + phi(g)) =e= 0;
        iq_initialization(g) .. iq(g,'1') - Ig(g)*cos(delta(g,'1') - alpha(g) + phi(g)) =e= 0;

* Limits of variables
        e_fd_lim_inf(g) .. e_fd_min(g) =l= e_fd(g);
        e_fd_lim_sup(g) .. e_fd(g) =l= e_fd_max(g);

* Discretized equations
*   Electrical equations
        Internal_voltaje_d(g,s)$(not sfirst(s)) .. ed_p(g,s)*(1 + Dt/(2*Tq_p(g))) - ed_p(g,s-1)*(1 - Dt/(2*Tq_p(g))) - (Dt/(2*Tq_p(g)))*(Xq(g) - Xq_p(g))*(iq(g,s) + iq(g,s-1)) =e= 0;
        Internal_voltaje_q(g,s)$(not sfirst(s)) .. eq_p(g,s)*(1 + Dt/(2*Td_p(g))) - eq_p(g,s-1)*(1 - Dt/(2*Td_p(g))) - (Dt/(2*Td_p(g)))*(2*e_fd(g) - (Xd(g) - Xd_p(g))*(id(g,s) + id(g,s-1))) =e= 0;

*   Mechanical equations
        oscilation_omega(g,s)$(not sfirst(s)) .. Domega(g,s)*(1 + Dt*D(g)/(4*H(g))) - Domega(g,s-1)*(1 - Dt*D(g)/(4*H(g))) - (Dt/(4*H(g)))*(2*Pg(g) - Pe(g,s) - Pe(g,s-1)) =e= 0;
        oscilation_delta(g,s)$(not sfirst(s)) .. delta(g,s) - delta(g,s-1) - (Dt*100*pi/2)*(Domega(g,s) + Domega(g,s-1)) =e= 0;

*   Electrical power output equations
        electric_power_fault(g,sf) .. Pe(g,sf) - ed_p(g,sf)*id(g,sf) - eq_p(g,sf)*iq(g,sf) =e= 0;
        electric_power_postfault(g,spf) .. Pe(g,spf) - ed_p(g,spf)*id(g,spf) - eq_p(g,spf)*iq(g,spf) =e= 0;

        P_balanced_1_at_HVDC_bus(hv,sf) .. Phvdc_1(hv,sf)
                                        - (sum(hvp,Y_f_red(hv,hvp)*Vhvdc(hvp,sf)*cos(alpha_hvdc(hv,sf) - alpha_hvdc(hvp,sf) - theta_f_red(hv,hvp)))
                                        +  sum(g,Y_f_red(hv,g)*(eq_p(g,sf)*cos(alpha_hvdc(hv,sf) - delta(g,sf) - theta_f_red(hv,g))
                                                              - ed_p(g,sf)*sin(alpha_hvdc(hv,sf) - delta(g,sf) - theta_f_red(hv,g)))))*Vhvdc(hv,sf) =e= 0;
        Q_balanced_1_at_hvdc_bus(hv,sf) .. Qhvdc_1(hv,sf)
                                        - (sum(hvp,Y_f_red(hv,hvp)*Vhvdc(hvp,sf)*sin(alpha_hvdc(hv,sf) - alpha_hvdc(hvp,sf) - theta_f_red(hv,hvp)))
                                        +  sum(g,Y_f_red(hv,g)*(eq_p(g,sf)*sin(alpha_hvdc(hv,sf) - delta(g,sf) - theta_f_red(hv,g))
                                                              + ed_p(g,sf)*cos(alpha_hvdc(hv,sf) - delta(g,sf) - theta_f_red(hv,g)))))*Vhvdc(hv,sf) =e= 0;
        P_balanced_2_at_HVDC_bus(hv,spf) .. Phvdc_1(hv,spf)
                                         - (sum(hvp,Y_pf_red(hv,hvp)*Vhvdc(hvp,spf)*cos(alpha_hvdc(hv,spf) - alpha_hvdc(hvp,spf) - theta_pf_red(hv,hvp)))
                                         +  sum(g,Y_pf_red(hv,g)*(eq_p(g,spf)*cos(alpha_hvdc(hv,spf) - delta(g,spf) - theta_pf_red(hv,g))
                                                                - ed_p(g,spf)*sin(alpha_hvdc(hv,spf) - delta(g,spf) - theta_pf_red(hv,g)))))*Vhvdc(hv,spf) =e= 0;
        Q_balanced_2_at_hvdc_bus(hv,spf) .. Qhvdc_1(hv,spf)
                                         - (sum(hvp,Y_pf_red(hv,hvp)*Vhvdc(hvp,spf)*sin(alpha_hvdc(hv,spf) - alpha_hvdc(hvp,spf) - theta_pf_red(hv,hvp)))
                                         +  sum(g,Y_pf_red(hv,g)*(eq_p(g,spf)*sin(alpha_hvdc(hv,spf) - delta(g,spf) - theta_pf_red(hv,g))
                                                                + ed_p(g,spf)*cos(alpha_hvdc(hv,spf) - delta(g,spf) - theta_pf_red(hv,g)))))*Vhvdc(hv,spf) =e= 0;

        Q_absorbed_at_HVDC_bus(hv,s) .. Qhvdc_1(hv,s) + Phvdc_1(hv,s)/2 =e= 0;
        P_inyected_1_at_HVDC_bus(hv,sf)$(not sfirst(sf)) .. Phvdc_1(hv,sf) =e= 0;
        P_inyected_2_at_HVDC_bus(hv,spf_1) .. Phvdc_1(hv,spf_1) =e= 0;
        P_inyected_3_at_HVDC_bus(hv,spf_2) .. Phvdc_1(hv,spf_2) - Phvdc(hv) - ((ord(spf_2)*0.02) - 1.0)*(Phvdc(hv)/1.0) =e= 0;
        P_inyected_4_at_HVDC_bus(hv,spf_3) .. Phvdc_1(hv,spf_3) - Phvdc(hv) =e= 0;

*   dq current equations
        id_stator_fault(g,sf)$(not sfirst(sf)) .. id(g,sf)
                                               - (sum(gp,Y_f_red(g,gp)*(ed_p(gp,sf)*cos(delta(g,sf) - delta(gp,sf) - theta_f_red(g,gp))
                                                                      + eq_p(gp,sf)*sin(delta(g,sf) - delta(gp,sf) - theta_f_red(g,gp))))
                                               +  sum(hv,Y_f_red(g,hv)*Vhvdc(hv,sf)*sin(delta(g,sf) - alpha_hvdc(hv,sf) - theta_f_red(g,hv)))) =e= 0;
        iq_stator_fault(g,sf)$(not sfirst(sf)) .. iq(g,sf)
                                               - (sum(gp,Y_f_red(g,gp)*(eq_p(gp,sf)*cos(delta(g,sf) - delta(gp,sf) - theta_f_red(g,gp))
                                                                      - ed_p(gp,sf)*sin(delta(g,sf) - delta(gp,sf) - theta_f_red(g,gp))))
                                               +  sum(hv,Y_f_red(g,hv)*Vhvdc(hv,sf)*cos(delta(g,sf) - alpha_hvdc(hv,sf) - theta_f_red(g,hv)))) =e= 0;
        id_stator_postfault_1(g,spf) .. id(g,spf)
                                     - (sum(gp,Y_pf_red(g,gp)*(ed_p(gp,spf)*cos(delta(g,spf) - delta(gp,spf) - theta_pf_red(g,gp))
                                                             + eq_p(gp,spf)*sin(delta(g,spf) - delta(gp,spf) - theta_pf_red(g,gp))))
                                     +  sum(hv,Y_pf_red(g,hv)*Vhvdc(hv,spf)*sin(delta(g,spf) - alpha_hvdc(hv,spf) - theta_pf_red(g,hv)))) =e= 0;
        iq_stator_postfault_1(g,spf) .. iq(g,spf)
                                     - (sum(gp,Y_pf_red(g,gp)*(eq_p(gp,spf)*cos(delta(g,spf) - delta(gp,spf) - theta_pf_red(g,gp))
                                                             - ed_p(gp,spf)*sin(delta(g,spf) - delta(gp,spf) - theta_pf_red(g,gp))))
                                     +  sum(hv,Y_pf_red(g,hv)*Vhvdc(hv,spf)*cos(delta(g,spf) - alpha_hvdc(hv,spf) - theta_pf_red(g,hv)))) =e= 0;

*   Stability criterion equations
        center_of_inertia(s) .. delta_COI(s) - sum(g,H(g)*delta(g,s)) / sum(g,H(g)) =e= 0;
        angular_deviation_min(g,s) .. - (angle_limit*pi/180) =l= delta(g,s) - delta_COI(s);
        angular_deviation_max(g,s) .. delta(g,s) - delta_COI(s) =l= (angle_limit*pi/180);

*Model tscopf /total_cost, p_balance_gen, p_balance_HVDC, p_balance_nongen, q_balance_gen, q_balance_HVDC, q_balance_nongen, PQ_HVDC_relation, ref_bus,
*                         P_gen_lim_inf, P_gen_lim_sup, Q_gen_lim_inf, Q_gen_lim_sup,
*                         Generators_current, Power_factor,
*                         ed_p_initialization, eq_p_initialization, Vd_initialization, Vq_initialization, Pe_initialization, *Domega_initialization, id_initialization, iq_initialization,
*                         e_fd_lim_inf, e_fd_lim_sup,
*                         Internal_voltaje_p, Internal_voltaje_q, oscilation_omega, oscilation_delta,
*                         electric_power_fault, id_stator_fault, iq_stator_fault,
*                         electric_power_postfault_1, id_stator_postfault_1, iq_stator_postfault_1,
*                         electric_power_postfault_2, id_stator_postfault_2, iq_stator_postfault_2,
*                         P_inyected_at_HVDC_bus, Q_inyected_at_HVDC_bus,
*                         center_of_inertia, angular_deviation_min, angular_deviation_max/;
Model tscopf /all/;

*$onecho >bench.opt
*  solvers ipopt
*$offecho
*tscopf.optfile = 1;
tscopf.workfactor = 100;
Option nlp = ipopt
       iterlim = 200000;
Solve tscopf using nlp minimizing z;

Display Pg.l, Phvdc.l, Qg.l, Qhvdc.l, V.l, alpha.l, ed_p.l, eq_p.l, delta.l, Domega.l, Pe.l, Phvdc_1.l;\n""")

        f.write("\nfile salida /calle_plot_" + str(angle_limit) + "_" + str_loadfactor[0] + "_" + str_loadfactor[1] + ".m/;")

        f.write("""
salida.nd = 6;
put salida

put 't = [...'/
loop(s, put (ord(s)*Dt)/)
put'];'/

put 'f_obj = [...'/
    put z.l/
put'];'/

put 'Pg = [...'/
loop(g, put Pg.l(g))
loop(hv, put Phvdc.l(hv)/)
put'];'/

put 'Qg = [...'/
loop(g, put Qg.l(g))
loop(hv, put Qhvdc.l(hv)/)
put'];'/

put 'delta = [...'/
loop(s,
    loop(g, put delta.l(g,s))
    put /);
put'];'/

put 'delta_COI = [...'/
loop(s, put delta_COI.l(s) /)
put'];'/

put 'Domega = [...'/
loop(s,
    loop(g, put Domega.l(g,s))
    put /);
put'];'/

put 'ed_p = [...'/
loop(s,
    loop(g, put ed_p.l(g,s))
    put /);
put'];'/

put 'eq_p = [...'/
loop(s,
    loop(g, put eq_p.l(g,s))
    put /);
put'];'/

put 'Pe = [...'/
loop(s,
    loop(g, put Pe.l(g,s))
    put /);
put'];'/

put 'Vhvdc = [...'/
loop(s,
    loop(hv, put Vhvdc.l(hv,s))
    put /);
put'];'/

put 'Phvdc_1 = [...'/
loop(s,
    loop(hv, put Phvdc_1.l(hv,s))
    put /);
put'];'/

put 'figure(2)'/
put 'plot(t, delta(:, 1))'/
put 'hold on'/
put 'plot(t, delta(:, 2))'/
put 'hold on'/
put 'plot(t, delta(:, 3))'/
put 'hold on'/
put 'plot(t, delta(:, 4))'/
put 'hold on'/
put 'plot(t, delta(:, 5))'/""")

        f.close()

