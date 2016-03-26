
function [elevations, times, normlift, normdrag, normlinetension] = kite(length, V, m, S, rho, elevation0, AoKdeg, n, duree,omega0)
% Cette fonction d�termine l'angle entre la ligne du kite et le sol en fonction du temps -> trajectoire du kite
% Cette fonction a pour param�tres d'entr�e :
% length : longueur de ligne du cerf-volant (m) constante
% V vitesse horizontale du vent (m/s)
% m : masse du cerf-volant (kg)
% S : surface du kite (m�)
% rho : masse volumique de l'air (kg/m^3)
% elevation : angle entre la ligne et le sol (d�crivant donc l'�l�vation du
% cerf-volant) (�). Positif si cerf-volant au dessus du sol
% AoKdeg : angle de calage (�) constant (pourrait �voluer si on le pilote).
% angle entre la corde du cerf-volant et la ligne. Positif pour un kite qui
% vole
% n : nombre d'it�rations
% dur�e : temps physique de l'exp�rience (s)
% omega0 : vitesse initiale du kite (rad/s). Positive si le cerf-volant
% monte

if nargin == 0      % si on sp�cifie aucun argument d'entr�e � kite, on prend les valeurs dans d�mo cf ci-apr�s)
    [elevations, times, normlift, normdrag, normlinetension] =demo();
    
    return
end


%�Initial condition
time = 0;
omega = omega0;
elevation = elevation0;
g = 9.81;
AoK = AoKdeg * pi/180;      % passage en radians
dt = duree/n;

%D�finition des variables globales pour les trac�s
OMEGA = zeros(1,n);
OMEGAp = zeros(1,n);
AngleA = zeros(1,n);
lifty = zeros(1,n);
liftz = zeros(1,n);
% normlift = zeros(1,n);
dragy = zeros(1,n);
dragz = zeros(1,n);
% normdraft = zeros(1,n);
linetensionsy=zeros(1,n);
linetensionsz=zeros(1,n);
normlinetension=zeros(1,n);

for i=1:n;
    
    % Vitesse du kite par rapport au sol projet� dans le rep�re du sol
    u_kite = [-omega*length*sin(elevation), omega*length*cos(elevation)];
    
    % Vitesse du vent par rapport au sol projet� dans le rep�re du sol
    Vwind = [V, 0];
    %vitesse relative du vent (vitesse de l'air par rapport au kite projet�
    %dans le rep�re du sol)
    Vair_kite = Vwind-u_kite;
    i_y = 1;% horiztontale
    i_z = 2;% verticale
    
    angle_air_kite = atan2(Vair_kite(i_z), Vair_kite(i_y));
    AoA = angle_air_kite+AoK-elevation; %Angle of Attack (positif pour portance positive).
    AngleA(i) = AoA;    %impl�mentation pour trac�
    % Angle entre la corde du kite et la vitesse relative de l'air par rapport
    % au kite.
    
    normU=norm(Vair_kite);
    
    L = 1/2*rho*S*normU^2*coefflift(AoA); %portance
    
    D = 1/2*rho*S*normU^2*coeffdrag(AoA); %train�e
    
    
    
    Ly = -L*sin(angle_air_kite); %Projections dans le rep�re du sol
    Lz = L*cos(angle_air_kite);
    lifty(i)=Ly;
    liftz(i)=Lz;
    normlift(i) = sqrt(Ly^2+Lz^2);
    
    Dy = D*cos(angle_air_kite);
    Dz = D*sin(angle_air_kite);
    dragy(i)=Dy;
    dragz(i)=Dz;
    normdrag(i) = sqrt(Ly^2+Lz^2);
    
    position = length * [cos(elevation); sin(elevation)];
    
    % moment suivant l'axe x (positive quand le kite monte)
    ML = (Lz+Dz) * position(1);
    MD = (Ly+Dy) * position(2);
    MW =-m*g * position(1);
    
    omegap = 1/(m*length^2) * (ML + MD + MW)- 0.0*omega;  %x*omega = amortissement
    
    omega = omega + omegap * dt;
    elevation = elevation + omega * dt;
    elevations(i)=elevation;
    
    OMEGA(i)=omega;
    OMEGAp(i)=omegap;
    
    time = time+dt;
    times(i)=time;
    
    %Calcul de la tension -> Probl�me : absence de tension d�s avant
    %l'�quilibre dynamique du kite
    linetension=[(Ly + Dy + m*omegap*length*cos(AoA))/cos(elevation);(Lz - Dz - m*g + m*omegap*length*sin(AoA))/sin(elevation)];
    linetensionsy(i)=linetension(1);
    linetensionsz(i)=linetension(2);
    normlinetension(i)=sqrt(linetensionsy(i)^2+linetensionsz(i)^2);
end

figure; % Trac� de diff�rentes grandeurs en fonction du temps

subplot(6,1,1);
plot(times, OMEGA)
title('Vitesse angulaire en fonction du temps')
subplot(6,1,2);
plot(times,AngleA*180/pi)
title('Angle d''attaque')
subplot(6,1,3);
plot(times, lifty)
title('Portance horizontale en fonction du temps')
subplot(6,1,4);
plot(times, liftz)
title('Portance verticale en fonction du temps')
subplot(6,1,5);
plot(times, dragy)
title('Trainee horizon  tale en fonction du temps')
xlabel('Temps (s)')
subplot(6,1,6);
plot(times, dragz)
title('Trainee verticale en fonction du temps')
xlabel('Temps (s)')

figure;
chart(elevations, times, normlift, normdrag, normlinetension)

end

function chart(elevations, times, normlift, normdrag, normlinetension)
subplot(4,1,1);
plot(times, normlinetension)
title('Tension dans la ligne en fonction du temps')
subplot(4,1,2);
plot(times, normlift)
title('Portance en fonction du temps')
subplot(4,1,3);
plot(times, normdrag)
title('Train�e en fonction du temps')
subplot(4,1,4);
plot(times, elevations*180/pi)
title('Elevation en fonction du temps (�)')
end

function [elevations, times, normlift, normdrag, normlinetension] =demo()
length = 10;
V = 10; %vitesse du vent
m = 4; %masse du kite
S = 6; %surface de l'aile
rho = 1;
elevation0 = 0;
omega0 = 0; %vitesse de rotation
AoKdeg = 50; %Angle of Keying (calage)
n=1000;
duree = 10;
[elevations, times, normlift, normdrag, normlinetension] = kite(length, V, m, S, rho, elevation0, AoKdeg, n, duree,omega0);
end

function [Cl] = coefflift(alpha)
Cl = pi*sin (2*alpha);
end

function [Cd] = coeffdrag(alpha)
Cd0 = 0.01; %amortissement
Cd = sin (alpha) + Cd0;
end
