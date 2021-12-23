clc
clear
close all

%% params
name='me+flan+fish.jpg';
loc='C:\\Users\Matthew\Desktop\';
duration=20; %seconds
framerate=60; %fps
max=255; %pixel vals
min=0;
ncyclesSlow=10;
ncyclesFast=150;

%get img/preprocess
nam=[loc,name];
im=imread(nam);
im=imresize(im,.90);
im=double(im);
[r,c,x]=size(im);

%im=round(mean(im,3));
im=imgaussfilt(im,1);

%set up vidwrite
v1=VideoWriter([name '_im2sinus.mp4'],'MPEG-4');
v1.FrameRate=framerate;
open(v1);
%set up video
L=duration*framerate;
A=(max-min)/2;
DC=mean([max,min]);
t=0:1/framerate:duration-1;

possible_vals=min:max; %value range
minfreq=ncyclesSlow/duration;
maxfreq=ncyclesFast/duration;
range=maxfreq-minfreq;
freqs_range=minfreq + range*(possible_vals/max) ;%radians

freqs=minfreq+range*(im/max);
t=t+.25;
for i=1:13
    a=DC+A*sin(2*pi*freqs*t(1)-pi/2);
    a=imgaussfilt(a);
    a=uint8(round(a));
    writeVideo(v1,a);
end

for i=1:length(t)
    a=DC+A*sin(2*pi*freqs*t(i)-pi/2);
    a=imgaussfilt(a);
    a=uint8(round(a));
    writeVideo(v1,a);
end

close(v1)