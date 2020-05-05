clc
clear
close all


%% improvements:
%make the three channels cluster together and somehow return color out?
%make regions gradually change size from one extreme to another?


%% params
L = 3; %seconds
framerate = 30; %fps

start_n = 10;
end_n = 2;

cd("..")

%% read img
im=double(imread('inputs/crouch_square.jpg'));
im=imresize(im,.33);
rows=size(im,1);
cols=size(im,2);

%% start up vid
now=datestr(datetime);
now(now==':')=[];
vOut=VideoWriter([pwd '\kmeaner_' now '.mp4'],'MPEG-4');
vOut.Quality = 100;
vOut.FrameRate=framerate;
open(vOut);

%% run
nFrames=L*framerate;
ks = round(start_n   :   ((end_n-start_n)/nFrames)   :    end_n);
ks=ks(1:nFrames);
for i = 1:nFrames
    
    if false
        if i>1
            if ks(i)~=ks(i-1)
                frame = getClusters(im,ks(i));
            end
        else
            frame = getClusters(im,ks(i));
        end
    else
        frame = getClusters(im,ks(i));
    end
    
    writeVideo(vOut,uint8(round(frame)));
    disp(i);
end
fprintf('\n');
disp('closing')


close(vOut);


function [k_im] = getClusters (image, k)
    ds=1000;


    image=reshape(image,[size(image,1),size(image,2)*3]);
    %feats: intensity, entropy, laplacian, hessian
    ent = entropyfilt(image);
    [Gmag,~] = imgradient(image);
    [gx, gy] = gradient(double(image));
    [gxx, gxy] = gradient(gx);
    [~, gyy] = gradient(gy);
    
    
    featvecs={ent, Gmag, gx, gy, gxx, gxy, gyy, image};
    feats=zeros(size(image,1)*size(image,2),length(featvecs));
    
    for i=1:length(featvecs)
       featvecs{i}=featvecs{i}/max(max(featvecs{i})); 
       feats(:,i)=featvecs{i}(:); 
    end
    
    
    
    feats_d=feats(1:ds:end,:);
    [~,C] = kmeans (feats_d,k);
    [classes,C]=kmeans(feats, k,'MaxIter',1,'Start',C);
    
    if true
        colors=C(:,8);
        newIm = colors(classes);
        k_im = 255*(reshape(newIm,[size(image,1),size(image,2)/3,3]));
    else
        newIm=classes;
        k_im = 255*(reshape(newIm,[size(image,1),size(image,2)/3,3])/k);
    end
    
    

end











