clc
clear
close all
%% params
L = 10; %seconds
% rows = 1000; %rows
% cols = 1000; %cols
framerate = 30; %fps
activate_dur = 12; %frames 
deactivate_dur = 3; %frames
n_seeds = 50; %number of starting seeds

%% read img
im=double(imread('inputs/poll_new.jpg'));
im=imresize(im,1);
rows=size(im,1);
cols=size(im,2);

%% some math
p=n_seeds/(rows*cols);

%% make initial array
start = zeros(rows,cols);
start_rows = randi(rows, [1, n_seeds]);
start_cols = randi(cols, [1, n_seeds]);

imshow(uint8(im))
[start_cols, start_rows] = getpts;
start_rows=round(start_rows);
start_cols=round(start_cols);

for i=1:(length(start_rows))
    start(start_rows(i),start_cols(i)) = 1;
end


%% prep for start
nFrames=L*framerate;
%frames(1:rows,1:cols,nFrames)=0;

onTimes=activate_dur*start;

%% start up vid
now=datestr(datetime);
now(now==':')=[];
vOut=VideoWriter([pwd '\activating_videos_' now '.mp4'],'MPEG-4');
vOut.Quality = 75;
vOut.FrameRate=framerate-10;
open(vOut);


%% run
filt=[0 1 1 1 0; 1 1 1 1 1; 0 0 1 0 0];
%filt=rand([10,10])>.5;
filt1=fspecial('disk',20);
filt2=fspecial('gaussian',41,8);
filt=filt1.*filt2;
%frames(:,:,1)=start;
oldframe=zeros(rows,cols);
for i = 2:nFrames
    onTimesNew=onTimes;
    %decrease time on already-ons
    
    onTimesNew(onTimes>0)=onTimesNew(onTimes>0)-1;
    
    %find find new off values and disable them
    new_offs = (onTimesNew==0) & (onTimes~=0);
    onTimesNew(new_offs) = -deactivate_dur;
    
    %step up old off values
    onTimesNew(onTimes<0) = onTimesNew(onTimes<0) + 1;
    
    %activate neighbors of current off values
    neighborsOn = conv2(onTimes>0,filt,'same');
    neighborsOn ((onTimes>0)) = 0; %do not activate current activated
    neighborsOn ((onTimes<-3)) = 0; %do not activate current deactivated
    %neighborsOn(rand([rows,cols])<.3) = 0; %stop some activations randomly
    onTimesNew(neighborsOn>0) = activate_dur;
    
    %write to frames files
    newframe=oldframe;
    newframe(onTimesNew>0)=onTimesNew(onTimesNew>0);
    newframe=newframe/activate_dur;
    %frames(:,:,1,i)=newframe;
    newframe3=cat(3, newframe, newframe, newframe);
    %imshow(newframe)
    frame=im.*newframe3;
    writeVideo(vOut,uint8(round(frame)));
    
    onTimes=onTimesNew;
    oldframe=newframe;
    fprintf('%d ',i);
end
fprintf('\n');
disp('closing')


close(vOut);
% vid=repmat(im, 1, 1, 1, nFrames);
% frames=cat(3, frames, frames, frames); %make 3d frames
% vid=vid.*frames; %weight these frames












