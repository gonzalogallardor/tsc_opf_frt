Vr_x.l(dfig) = 0.1; Vr_x.lo(dfig) = 0;
alphaVr_x.l(dfig) = 0.1; alphaVr_x.lo(dfig) = -pi; alphaVr_x.up(dfig) = pi;
Ir_x.l(dfig) = 1; Ir_x.lo(dfig) = 0;
alphaIr_x.l(dfig) = 0.1; alphaIr_x.lo(dfig) = -pi; alphaIr_x.up(dfig) = pi;
Is.l(dfig) = 1; Is.lo(dfig) = 0;
alphaIs.l(dfig) = 0.1; alphaIs.lo(dfig) = -pi; alphaIs.up(dfig) = pi;
u_wind.l(dfig) = 10; u_wind.lo(dfig) = 3; u_wind.up(dfig) = 14;

lambda.l(dfig,s) = Kb(dfig)*wr_ref(dfig)/10;
Cp.l(dfig,s) = 0.5;
pitch_angle.l(dfig,'1') = 0; pitch_angle.lo(dfig,s) = 0; pitch_angle.up(dfig,s) = 27;
P_mech.l(dfig,s) = Ps_w_ini_SM(dfig); P_mech.lo(dfig,s) = 0;

T_el.l(dfig,s) = Ps_w_ini_SM(dfig)/1.2;
T_mech.l(dfig,s) = Ps_w_ini_SM(dfig)/1.2;
wr.l(dfig,s) = 1.2; wr.lo(dfig,s) = 0;
delta_wr.l(dfig,s) = 0.2;

vD_w.l(dfig,'1') = 1;
vQ_w.l(dfig,'1') = 0;
vD_w.l(dfig,sf) = 0.4/2;
vQ_w.l(dfig,sf) = 0.4/2;
vD_w.l(dfig,spf) = 1/2;
vQ_w.l(dfig,spf) = 1/2;

iD_w.l(dfig,s) = 0.8*Ps_w_ini_SM(dfig);
iQ_w.l(dfig,s) = 0;

v_w.l(dfig,'1') = 1; v_w.lo(dfig,s) = 0;
v_w.l(dfig,sf) = 0.4;
v_w.l(dfig,spf) = 0.9;

alpha_w.l(dfig,s) = 10*pi/180;

iDs_w.l(dfig,s) = Ps_w_ini_SM(dfig);
iQs_w.l(dfig,s) = 0;

Ps_w.l(dfig,s) = Ps_w_ini_SM(dfig);
Qs_w.l(dfig,s) = 0;

is_w.l(dfig,s) = Ps_w_ini_SM(dfig); is_w.lo(dfig,s) = 0;
is_w.l(dfig,sf) = 3*Sb_w(dfig)/Sb;
is_w.l(dfig,spf) = Ps_w_ini_SM(dfig);

alpha_is_w.l(dfig,s) = 10*pi/180;

Pg_w.l(dfig,s) = Pg_w_ini_SM(dfig);
Qg_w.l(dfig,s) = 0;

Pgsc_w.l(dfig,'1') = -0.2*Ps_w_ini_SM(dfig);
Pgsc_w.l(dfig,sdfig_1)$(not sfirst(sdfig_1)) = 0;
Pgsc_w.l(dfig,sdfig_2) = -0.2*Ps_w_ini_SM(dfig);
Pgsc_w.up(dfig,sdfig_1) = 0;

Pr_loss.l(dfig,s) = 0;

pll_angle.l(dfig,sdfig_2) = pi/2;
u_pll.l(dfig,sdfig_2) = 0;

vD_w_control.l(dfig,sdfig_2) = 0;
vQ_w_control.l(dfig,sdfig_2) = 1;

eD_p_w.l(dfig,sdfig_1) = -1;
eQ_p_w.l(dfig,sdfig_1) = xs_p(dfig)*Ps_w_ini_SM(dfig);
eD_p_w_control.l(dfig,sdfig_2) = xs_p(dfig)*Ps_w_ini_SM(dfig);
eQ_p_w_control.l(dfig,sdfig_2) = 1;

iDs_w_control.l(dfig,sdfig_2) = 0;
iQs_w_control.l(dfig,sdfig_2) = Ps_w_ini_SM(dfig);

Edr.l(dfig,'1') = 1;
Eqr.l(dfig,'1') = 1;
Edr.l(dfig,sdfig_1)$(not sfirst(sdfig_1)) = 0;
Eqr.l(dfig,sdfig_1)$(not sfirst(sdfig_1)) = 0;
Edr_control.l(dfig,sdfig_2) = 1 + w0*0.2*To_p(dfig)*(xs_p(dfig)*Ps_w_ini_SM(dfig));
Eqr_control.l(dfig,sdfig_2) = xs(dfig)*Ps_w_ini_SM(dfig) - w0*0.2*To_p(dfig)*(1);
delta_wr_pre.l(dfig) = (wr_ref(dfig) - 1);

Ir_1.l(dfig) = 1; Ir_1.lo(dfig) = 0;
angleIr_1.l(dfig) = 0;
Idr_control_pre.l(dfig) = 1;
Iqr_control_pre.l(dfig) = 1;
Ep_1.l(dfig) = 1; Ep_1.lo(dfig) = 0;
angleEp_1.l(dfig) = 0;
eD_p_w_control_pre.l(dfig) = xs_p(dfig)*Ps_w_ini_SM(dfig);
eQ_p_w_control_pre.l(dfig) = 1;

Idr.l(dfig,sdfig_1) = 1;
Iqr.l(dfig,sdfig_1) = xs(dfig)*Ps_w_ini_SM(dfig);
Idr_control.l(dfig,sdfig_2) = 1;
Iqr_control.l(dfig,sdfig_2) = 1;

error_Idr.l(dfig,sdfig_2) = 0;
error_Iqr.l(dfig,sdfig_2) = 0;

v_w_ord.l(dfig,sdfig_2) = 1;
error_Qs_w.l(dfig,sdfig_2) = 0.2*Ps_w_ini_SM(dfig)/Sb;
error_v_w.l(dfig,sdfig_2) = 0.1;
Idr_ref.l(dfig,sdfig_2) = 1;

iQs_w_control_ord.l(dfig,sdfig_2) = Ps_w_ini_SM(dfig);
Iqr_ref.l(dfig,sdfig_2) = xs(dfig)*Ps_w_ini_SM(dfig);

T_ord.l(dfig,sdfig_2) = Ps_w_ini_SM(dfig)/1.2;
P_ord.l(dfig,sdfig_2) = Ps_w_ini_SM(dfig);
error_wr.l(dfig,s) = 0;

pitch_cmd.l(dfig,s) = 0;
pitch_comp.l(dfig,'1') = 0;
pitch_comp.l(dfig,sdfig_1) = 0;
pitch_comp.l(dfig,sdfig_2) = -5;
delta_P.l(dfig,sdfig_2) = Ps_w_ini_SM(dfig) - Ps_w_max_SM(dfig);