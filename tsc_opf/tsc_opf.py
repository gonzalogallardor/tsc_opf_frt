from functionalities.read_module import *
from functionalities.construction_module import *
from functionalities.write_module import *
import numpy as np
import copy

data_path = '../tests/gallardo/raw_data.raw'
gen_parameters_path = '../tests/gallardo/thermal_units_param.csv'
hvdc_param_path = '../tests/gallardo/hvdc_param.csv'
dfig_param_path = '../tests/gallardo/dfig_param.csv'
tsc_param_path = '../tests/gallardo/tsc_param.csv'
opf_param_path = '../tests/gallardo/opf_param.csv'

### DATA READ
s_base, buses, loads, generators, \
    branches, transformers = read_raw_data(data_path)
add_gen_parameters(gen_parameters_path, generators)
#hvdc_param = read_hvdc_param(hvdc_param_path)
dfig_param = read_dfig_param(dfig_param_path)
opf_param = read_opf_param(opf_param_path)
tsc_param = read_tsc_param(tsc_param_path)

### EXTRACTING DATA 
total_time = float(tsc_param['total_time'])
clearing_time = float(tsc_param['clearing_time'])
delta_t = float(tsc_param['delta_t'])
faulted_bus_number = int(tsc_param['faulted_bus'])
[faulted_bus_index] = get_index(buses, [faulted_bus_number])
isolated_branch = get_branch_index(branches,
                                   tsc_param['isolated_branch_bus1'],
                                   tsc_param['isolated_branch_bus2'])
dfig_bus_number = int(dfig_param['bus_number'])  # bus_number
[dfig_bus_index] = get_index(buses, [dfig_bus_number])
f = 50

# postfault_time_analisis / total_postfault_time

load_factors = tuple(np.arange(0.1, 2.55, 0.05))
angle_limits = (60,)
for load_factor in load_factors:
    for angle_limit in angle_limits:
        
        ### Initial Ybus construction considering all buses, branches and transformers,
        ### indexed according to read_data function and saved in the respective system
        ### class of each element

        Y = Ybus_construction(buses, branches, transformers)

        # Adding "load_factor" effect to Y matrix
        for load in loads:
            y_shunt_equivalent =  np.conjugate(complex(load.p, 
                                                       load.q)) * \
                                                       load_factor / s_base
            Y = Ybus_add_shunt_element(Y, 
                                       y_shunt_equivalent,
                                       load.bus_index)

#        Y[hvdc_bus_index, hvdc_bus_index] += complex(0.0,1.23)    #  HVDC link capacitor: Q_consumption = 1/2 P_hvdc


        ###
        ### Creation of extended Ybus matrix (prefault) : [Y_ext]
        ###

        total_buses = len(buses) + len(generators)
        Y_ext = np.zeros((total_buses, total_buses), complex)
        Y_ext[:len(buses), :len(buses)] = Y

        # Adding generator transformer impedances to Y_ext
        for generator in generators:
            
            y_tran = 1 / complex(generator.r_tran, 
                                 generator.x_tran) * \
                        generator.mva_base / s_base

            Y_ext = Ybus_add_series_element(Y_ext, 
                                            y_tran, 
                                            generator.bus_index, 
                                            generator.internal_bus_index)


        ###
        ### Creation of faulted Ybus matrix (during the fault): [Y_fault_ext] and [Y_fault_reduced]
        ###

        Y_fault_ext = copy.deepcopy(Y_ext)
        Y_fault_ext[faulted_bus_index, faulted_bus_index] += complex(0,-1e6)  # 3-f fault representation

        retained_bus_indexes = []
        retained_bus_numbers = []
        for generator in generators:
            retained_bus_indexes.append(generator.internal_bus_index)
            retained_bus_numbers.append(generator.bus_number)

        
        retained_bus_indexes.append(dfig_bus_index)
        retained_bus_numbers.append(dfig_bus_number)
        
        # Creation of a reduced faulted Ybus matrix considering generators internal buses and HVDC-link bus (only)
        Y_fault_reduced = kron_reduction(Y_fault_ext, 
                                         retained_bus_indexes)

        ###
        ### Creation of post fault Ybus matrix: [Y_postfault_ext] and [Y_postfault_reduced]
        ###

        Y_postfault_ext = copy.deepcopy(Y_ext)

        # removing isolated branch from Ybus
        y_series = 1 / complex(isolated_branch.r, isolated_branch.x)
        y_shunt = 1 / 2 * complex(isolated_branch.g, isolated_branch.b)

        Y_postfault_ext = Ybus_add_series_element(Y_postfault_ext,
                                                  - y_series,
                                                  isolated_branch.bus_index_1,
                                                  isolated_branch.bus_index_2)

        Y_postfault_ext = Ybus_add_shunt_element(Y_postfault_ext,
                                                 - y_shunt,
                                                 isolated_branch.bus_index_1)

        Y_postfault_ext = Ybus_add_shunt_element(Y_postfault_ext,
                                                 - y_shunt,
                                                 isolated_branch.bus_index_2)

        Y_postfault_reduced = kron_reduction(Y_postfault_ext, 
                                             retained_bus_indexes)


        ###
        ### Writing the gams file
        ###

        gams_file = "test_tscopf_" + str(angle_limit) + "_" + str(load_factor) + ".gms"
        file = open(gams_file,'w')

        scalars = write_scalars(s_base,       # MVA
                                delta_t,      # in seconds
                                angle_limit,  # degrees
                                f)            # frequency[Hz]

        sets = write_sets(buses,                 # all buses instances in the list
                          generators,            # all generator instances in the list
                          branches,              # all branch instances in the list
                          dfig_param,            # dfig parameters
                          retained_bus_numbers,  # retained bus numbers as list
                          total_time,            # seconds
                          clearing_time,         # seconds
                          delta_t)               # seconds

        
        sets += "\nsfirst(s) = yes$(ord(s) eq 1);\n" + \
                "alias (sg,sgp);\n" + \
                "alias (dfig,dfigp);\n"

        parameters = write_parameters(buses,
                                      generators,
                                      branches,
                                      tsc_param,
                                      dfig_param,  # dfig parameters as structured array
                                      s_base)


        tables = write_tables(Y,                     # Y bus, all buses, pre fault stage  (array)
                              Y_fault_reduced,       # Y bus, retained buses only, during fault (array)
                              Y_postfault_reduced,   # Y bus, retained buses only, post fault stage (array)
                              buses,                 # All buses instances(class) as list
                              retained_bus_numbers)  # All retained in a list

        variables, var_restrictions, equation_names, equations = write_equations(generators,
                                                                                branches,
                                                                                dfig_param,
                                                                                opf_param,
                                                                                s_base)

        file.write(scalars)
        file.write(sets)
        file.write(parameters)
        file.write(tables)
        file.write(variables)
        file.write(var_restrictions)
        file.write(equation_names)
        file.write(equations)

        str_loadfactor = str(load_factor)
        str_loadfactor_split = str_loadfactor.split('.')

        file.write("\n\nModel tscopf /all/;\n\
        tscopf.workfactor = 100;\n\
        Option nlp = ipopt\n\
        iterlim = 10000;\n\
        Solve tscopf using nlp minimizing z;\n\
        Display Pg.l, Qg.l, V.l, alpha.l, ed_p.l, eq_p.l, delta.l, Domega.l, Pe.l;")

        file.write("\n\nfile salida /galla_plot_" + str(angle_limit) + "_" + str_loadfactor_split[0] + "_" + str_loadfactor_split[1] + ".m/;")
        file.write("""
salida.nd = 8;
put salida
put 'f_obj = [...'/put z.l/put'];'/
put 'Pg = [...'/loop(rb, put Pg.l(rb))put'];'/
put 'Qg = [...'/loop(rb, put Qg.l(rb))put'];'/
put 'V = [...'/loop(b, put V.l(b))put'];'/
put 'alpha = [...'/loop(b, put alpha.l(b))put'];'/
put 't = [...'/loop(s, put (ord(s)*Dt)/)put'];'/
put 'delta = [...'/loop(s,loop(sg, put delta.l(sg,s))put /);put'];'/
put 'delta_COI = [...'/loop(s, put delta_COI.l(s) /)put'];'/
put 'Domega = [...'/loop(s,loop(sg, put Domega.l(sg,s))put /);put'];'/
put 'ed_p = [...'/loop(s,loop(sg, put ed_p.l(sg,s))put /);put'];'/
put 'eq_p = [...'/loop(s,loop(sg, put eq_p.l(sg,s))put /);put'];'/
put 'Pe = [...'/loop(s,loop(sg, put Pe.l(sg,s))put /);put'];'/

put 'figure(1)'/
put 'plot(t, delta(:, 1))'/
put 'hold on'/
put 'plot(t, delta(:, 2))'/
put 'hold on'/
put 'plot(t, delta(:, 3))'/
put 'hold on'/
put 'plot(t, delta(:, 4))'/
put 'hold on'/
put 'plot(t, delta(:, 5))'/

put ' V_w = [...'/loop(s,    loop(dfig, put V_w.l(dfig,s))    put /);put'];'/
put ' alpha_w = [...'/loop(s,    loop(dfig, put alpha_w.l(dfig,s))    put /);put'];'/
put ' Pg_w_var = [...'/loop(s,    loop(dfig, put Pg_w_var.l(dfig,s))    put /);put'];'/
put ' Qg_w_var = [...'/loop(s,    loop(dfig, put Qg_w_var.l(dfig,s))    put /);put'];'/

put "figure(2), plot(t(1:end, 1), V_w(:, 1)), title('V_w')"/
put "figure(3), plot(t(1:end, 1), alpha_w(:, 1)), title('alpha_w')"/
put "figure(4), plot(t(1:end, 1), Pg_w_var(:, 1)), title('Pg_w_var')"/
put "figure(5), plot(t(1:end, 1), Qg_w_var(:, 1)), title('Qg_w_var')"/""")


        file.close()