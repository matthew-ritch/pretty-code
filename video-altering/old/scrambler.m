clc
clear
close all
L=100;
nfrags=9;
nam='flan+sam';
im=imread([nam '.jpg']);
im=imresize(im,.33);
[r,c,x]=size(im);
v1=VideoWriter([nam '_scrambled.mp4'],'MPEG-4');
v1.FrameRate=17;
open(v1);
rWidth=floor(r/(sqrt(nfrags)));
cWidth=floor(c/(sqrt(nfrags)));



for i=1:L
    [jVec,kVec]=(meshgrid(randperm(sqrt(nfrags)),randperm(sqrt(nfrags))));
    a=[];
    for j=1:sqrt(nfrags)
        widA=[];
        for k=1:sqrt(nfrags)
            rRange=1+(j-1)*rWidth:j*rWidth;
            cRange=1+(k-1)*cWidth:k*cWidth;
            newj=jVec(j,k);
            newk=kVec(j,k);
            newrRange=1+(newj-1)*rWidth:newj*rWidth;
            newcRange=1+(newk-1)*cWidth:newk*cWidth;
            widA=[widA,(im(newrRange,newcRange,:))];
        end
        a=[a;widA];
    end
    
    writeVideo(v1,a);
end

close(v1)