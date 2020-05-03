clc
clear
close all
L=150;
nfrags=25;
nam='flan+sam';
im=imread([nam '.jpg']);
im=imresize(im,.33);
[r,c,x]=size(im);
v1=VideoWriter([nam '_coarsed.mp4'],'MPEG-4');
v1.FrameRate=30;
open(v1);
rWidth=floor(r/(sqrt(nfrags)));
cWidth=floor(c/(sqrt(nfrags)));



for i=1:L
    a=[];
    for j=1:sqrt(nfrags)
        aWid=[];
        for k=1:sqrt(nfrags);
            xmin=0.3;
            xmax=1;
            f=xmin+rand(1).*(xmax-xmin);
            rRange=1+(j-1)*rWidth:j*rWidth;
            cRange=1+(k-1)*cWidth:k*cWidth;
            aWid=[aWid,(im(rRange,cRange,:)).*f];
            
        end
        a=[a;aWid];
    end
    writeVideo(v1,a);
end

close(v1)