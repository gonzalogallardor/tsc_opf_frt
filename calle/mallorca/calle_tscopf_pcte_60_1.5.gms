Scalars
         Sb "Potencia base en [MVA]" /100/
         Dt "Paso de integracion en [s]" /0.020000/
         angle_limit /60/

     
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
    Tq_p(g) /1 1.0, 2 1.0, 3 1.0, 4 1.0, 5 1.0/;

Table Y(b,b)
             1          2          3          4          5          6          7          8          9         10         11         12         13         14         15         16         17         18         19         20 
  1   85.68980    0.00000    0.00000    0.00000    0.00000    0.00000   85.68980    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
  2    0.00000   72.83321    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   72.83321    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
  3    0.00000    0.00000   72.83321    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   72.83321    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
  4    0.00000    0.00000    0.00000   39.29273    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   39.29273    0.00000    0.00000    0.00000    0.00000 
  5    0.00000    0.00000    0.00000    0.00000   39.29273    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   39.29273    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
  6    0.00000    0.00000    0.00000    0.00000    0.00000  209.50677  136.32822    0.00000    0.00000    0.00000    0.00000    0.00000   37.49531    0.00000    0.00000    0.00000   37.49531    0.00000    0.00000    0.00000 
  7   85.68980    0.00000    0.00000    0.00000    0.00000  136.32822  370.15731   81.75117    0.00000   29.91482    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   37.49531    0.00000    0.00000 
  8    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   81.75117  190.98423   36.07302   36.07302    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   37.49531    0.00000 
  9    0.00000   72.83321    0.00000    0.00000    0.00000    0.00000    0.00000   36.07302  108.60222    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
 10    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   29.91482   36.07302    0.00000  317.61714  122.62676  129.10867    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
 11    0.00000    0.00000   72.83321    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000  122.62676  195.91531    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
 12    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000  129.10867    0.00000  194.19042    0.00000    0.00000   37.49531    0.00000    0.00000    0.00000    0.00000   28.12148 
 13    0.00000    0.00000    0.00000    0.00000    0.00000   37.49531    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000  170.41117  137.87858    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
 14    0.00000    0.00000    0.00000    0.00000   39.29273    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000  137.87858  173.90430    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
 15    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   37.49531    0.00000    0.00000   90.36594   52.93321    0.00000    0.00000    0.00000    0.00000 
 16    0.00000    0.00000    0.00000   39.29273    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   52.93321   92.54774    0.00000    0.00000    0.00000    0.00000 
 17    0.00000    0.00000    0.00000    0.00000    0.00000   37.49531    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   63.40817   21.41957    5.23601    0.00000 
 18    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   37.49531    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   21.41957   81.36056   23.56182    0.00000 
 19    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   37.49531    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    5.23601   23.56182   71.28139    5.92761 
 20    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   28.12148    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    5.92761   34.27995 ;

Table theta(b,b)
             1          2          3          4          5          6          7          8          9         10         11         12         13         14         15         16         17         18         19         20 
  1   -1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
  2    0.00000   -1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
  3    0.00000    0.00000   -1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
  4    0.00000    0.00000    0.00000   -1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000 
  5    0.00000    0.00000    0.00000    0.00000   -1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
  6    0.00000    0.00000    0.00000    0.00000    0.00000   -1.47172    1.72339    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000 
  7    1.57080    0.00000    0.00000    0.00000    0.00000    1.72339   -1.46877    1.72345    0.00000    1.72335    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000 
  8    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.72345   -1.44803    1.72325    1.72325    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000 
  9    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    1.72325   -1.52033    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
 10    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.72335    1.72325    0.00000   -1.41801    1.72345    1.72374    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
 11    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.72345   -1.45623    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
 12    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.72374    0.00000   -1.46933    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    1.57080 
 13    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   -1.10825    2.15497    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
 14    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    2.15497   -1.09800    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000 
 15    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000   -1.53187    1.63728    0.00000    0.00000    0.00000    0.00000 
 16    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.63728   -1.51332    0.00000    0.00000    0.00000    0.00000 
 17    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000   -1.35167    2.01825    2.01829    0.00000 
 18    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    2.01825   -1.30061    2.01843    0.00000 
 19    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    2.01829    2.01843   -1.32595    2.01830 
 20    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    1.57080    0.00000    0.00000    0.00000    0.00000    0.00000    0.00000    2.01830   -1.41881 ;

Table Y_f_red(rb,rb)
             1          2          3          4          5          6 
  1   15.06187    0.42894    0.00005    0.00874    0.00000   10.57234 
  2    0.42894    8.73198    0.00005    0.01165    0.00000    4.17729 
  3    0.00005    0.00005   12.42089    0.00007    0.00000    0.00046 
  4    0.00874    0.01165    0.00007    5.96330    0.00000    0.10695 
  5    0.00000    0.00000    0.00000    0.00000    7.80229    7.54245 
  6   10.57234    4.17729    0.00046    0.10695    7.54245   61.00870 ;

Table theta_f_red(rb,rb)
             1          2          3          4          5          6 
  1   -1.55913    1.44844    1.55770    1.39364    0.00000    1.56883 
  2    1.44844   -1.51984    1.59051    1.37357    0.00000    1.60073 
  3    1.55770    1.59051   -1.55266    1.49146    0.00000    1.71221 
  4    1.39364    1.37357    1.49146   -1.52773    0.00000    1.60760 
  5    0.00000    0.00000    0.00000    0.00000   -1.51666    1.52716 
  6    1.56883    1.60073    1.71221    1.60760    1.52716   -1.36426 ;

Table Y_pf_red(rb,rb)
             1          2          3          4          5          6 
  1   14.79489    0.64449    0.55207    0.26320    0.00000   13.11107 
  2    0.64449    8.47267    0.88638    0.41865    0.00000    6.25114 
  3    0.55207    0.88638    9.32173    1.49333    0.00000    5.44624 
  4    0.26320    0.41865    1.49333    5.34143    0.00000    2.61516 
  5    0.00000    0.00000    0.00000    0.00000    7.80229    7.54245 
  6   13.11107    6.25114    5.44624    2.61516    7.54245   37.40306 ;

Table theta_pf_red(rb,rb)
             1          2          3          4          5          6 
  1   -1.55563    1.42979    1.32576    1.27321    0.00000    1.56353 
  2    1.42979   -1.51329    1.36252    1.30723    0.00000    1.58311 
  3    1.32576    1.36252   -1.45997    1.26342    0.00000    1.48512 
  4    1.27321    1.30723    1.26342   -1.47686    0.00000    1.43564 
  5    0.00000    0.00000    0.00000    0.00000   -1.51666    1.52716 
  6    1.56353    1.58311    1.48512    1.43564    1.52716   -1.31068 ;

Variables
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

Display Pg.l, Phvdc.l, Qg.l, Qhvdc.l, V.l, alpha.l, ed_p.l, eq_p.l, delta.l, Domega.l, Pe.l, Phvdc_1.l;

file salida /calle_plot_60_1_..m/;
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
put 'plot(t, delta(:, 5))'/