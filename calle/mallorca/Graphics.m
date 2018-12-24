figure(1)
plot(t,delta(:,1)*180/pi,'-b',t,delta(:,2)*180/pi,'--r',t,delta(:,3)*180/pi,'-.k',t,delta(:,4)*180/pi,'-.g',t,delta(:,5)*180/pi,'--b', ...
     t,delta_COI*(180/pi),'-g',t,delta_COI*(180/pi)+60,'-k',t,delta_COI*(180/pi)-60,'-k','LineWidth',1);
grid on
xlabel('\fontsize{12}Time t (s)')
ylabel('\fontsize{12}Angular deviation  \delta (degrees)')
legend('\fontsize{12}\delta_1','\fontsize{12}\delta_2','\fontsize{12}\delta_3','\fontsize{12}\delta_4','\fontsize{12}\delta_5', ...
       '\fontsize{12}\delta_C_O_I','Location','NorthOutside','Orientation','Horizontal');
saveas(gcf,'Angulos.fig')
saveas(gcf,'Angulos.emf')
saveas(gcf,'Angulos.eps')

figure(2)
plot(t,Domega(:,1),'-b',t,Domega(:,2),'--r',t,Domega(:,3),'-.k',t,Domega(:,4),'-.g',t,Domega(:,5),'--b', ...
     'LineWidth',1);
grid on
xlabel('\fontsize{12}Time t (s)')
ylabel('\fontsize{12}Speed deviation  \Delta\omega (pu)')
legend('\fontsize{12}\Delta\omega_1','\fontsize{12}\Delta\omega_2','\fontsize{12}\Delta\omega_3','\fontsize{12}\Delta\omega_4','\fontsize{12}\Delta\omega_5', ...
       'Location','NorthOutside','Orientation','Horizontal');
saveas(gcf,'Dw.fig')
saveas(gcf,'Dw.emf')
saveas(gcf,'Dw.eps')

figure(3)
plot(t,ed_p,t,eq_p);
grid on
xlabel('\fontsize{12}Time t (s)')
ylabel('\fontsize{12}Internal voltage (pu)')
saveas(gcf,'e_dq_p.fig')
saveas(gcf,'e_dq_p.emf')
saveas(gcf,'e_dq_p.eps')

figure(4)
plot(t,Vhvdc);
grid on
xlabel('\fontsize{12}Time t (s)')
ylabel('\fontsize{12}V^A^C_h_v_d_c (pu)')
saveas(gcf,'Vhvdc.fig')
saveas(gcf,'Vhvdc.emf')
saveas(gcf,'Vhvdc.eps')

figure(5)
plot(t,Pe(:,1),'-b',t,Pe(:,2),'--r',t,Pe(:,3),'-.k',t,Pe(:,4),'-.g',t,Pe(:,5),'--b',t,Phvdc_1,'-k', ...
     'LineWidth',1);
grid on
xlabel('\fontsize{12}Time t (s)')
ylabel('\fontsize{12}Electrical power output  Pe (pu)')
legend('\fontsize{12}P_e_1','\fontsize{12}P_e_2','\fontsize{12}P_e_3','\fontsize{12}P_e_4','\fontsize{12}P_e_5','\fontsize{12}P_H_V_D_C', ...
       'Location','NorthOutside','Orientation','Horizontal');
saveas(gcf,'Pe.fig')
saveas(gcf,'Pe.emf')
saveas(gcf,'Pe.eps')