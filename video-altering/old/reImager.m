clc
clear
close all
L=50;
nam='flan+sam';
im=imread([nam '.jpg']);
im=imresize(im,.33);
[r,c,x]=size(im);
v1=VideoWriter([nam '.mp4'],'MPEG-4');
v1.FrameRate=30;
open(v1);

for i=1:L
xmin=0.1;
xmax=1;
f=xmin+rand([r,c,x]).*(xmax-xmin);
scales{i}=f;
end

for i=1:L
    a=uint8(double(im).*scales{i});
    writeVideo(v1,a);
end

close(v1)