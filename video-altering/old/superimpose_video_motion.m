clc
clear
close all

%% setup
v2n='3.mp4';
v1n='1.mp4';
thresh=10;
framerate=30;
f=1;
flip=false;

v1ns=[v1n(1:end-4),'.mat'];
v2ns=[v2n(1:end-4),'.mat'];


%% read in files. superimposes 2 on 1
if ~exist(v1ns)
    v1=VideoReader(v1n);
    vid1=read(v1);
    save(v1ns,'vid1')
else
    load(v1ns)
end
if ~exist(v2ns)
    v2=VideoReader(v2n);
    vid2=read(v2);
    save(v2ns,'vid2')
else
    load(v2ns)
end

if flip
   temp=vid1;
   vid1=vid2;
   vid2=temp;
end

%% size/length considerations
%resize
vid1=imresize(vid1,f);
vid2=imresize(vid2,f);
%get lengths
l1=size(vid1,4);
l2=size(vid2,4);
L=min(l1,l2);
%cut both to the shorter length
vid1=vid1(:,:,:,1:L); 
vid2=vid2(:,:,:,1:L);


%% find motions in 2
movedframes={};
for i=2:L %skip the first because no reference frame
    diffs=double(vid2(:,:,:,i)-vid2(:,:,:,i-1));
    norms = vecnorm(diffs,2,3);
    mask=norms>thresh;
    mask=conv2(mask,[1 1 1; 1 1 1; 1 1 1],'same');
    mask=mask>3;
    movedframes{i}=mask;
end
movedframes{1}=movedframes{2};

%%blur movedframes
new=movedframes;
for i=2:L-1
    new{i}=movedframes{i+1}|movedframes{i}|movedframes{i-1};
end
movedframes=new;
disp('found moving frames')
%% add to 1 based on motion in 2
frames=zeros([size(norms,1), size(norms,2), 3, L]);
for i=1:L-1
   newfram=vid1(:,:,:,i);
   vid2fram=vid2(:,:,:,i);
   mask=cat(3,movedframes{i+1},movedframes{i+1},movedframes{i+1});
   newfram(mask)=vid2fram(mask);
   frames(:,:,:,i)=newfram;
end

disp('edited moved frames')
%% write vid
now=datestr(datetime);
now(now==':')=[];
vOut=VideoWriter([pwd '\superimposed_videos_' now '.mp4'],'MPEG-4');
vOut.FrameRate=framerate;
open(vOut);
writeVideo(vOut,uint8(frames));
close(vOut);

close all