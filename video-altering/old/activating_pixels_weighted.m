clc
clear
close all
%% params
L = 10; %seconds
rows = 500; %rows
cols = 500; %cols
framerate = 30; %fps
activate_dur = 10; %frames 
deactivate_dur = 3; %frames
n_seeds = 50; %number of starting seeds

%% some math
p=n_seeds/(rows*cols);

%% make initial array
start = zeros(rows,cols);
start_rows = randi(rows, [1, n_seeds]);
start_cols = randi(cols, [1, n_seeds]);

for i=1:(n_seeds)
    start(start_rows(i),start_cols(i)) = 1;
end

%% prep for start
nFrames=L*framerate;
frames(1:rows,1:cols,nFrames)=0;

onTimes=activate_dur*start;

%% run
frames(:,:,1)=start;
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
    neighborsOn = conv2(onTimes>0,[1 1 1; 1 1 1; 1 1 1],'same');
    neighborsOn ((onTimes>0)) = 0; %do not activate current activated
    neighborsOn ((onTimes<-3)) = 0; %do not activate current deactivated
    onTimesNew(neighborsOn>0) = activate_dur;
    
    %write to frames files
    newframe=frames(:,:,i);
    newframe(onTimesNew>0)=1;
    frames(:,:,i)=newframe;
    imshow(newframe)
    
    onTimes=onTimesNew;
end


% %% run
% frames(:,:,1)=start;
% for i = 2:nFrames
%     %calculate time remaining on
%     onTimesRem = onTimes - 1;
%     onTimesRem(onTimesRem<0)=0;
%     %find new off values
%     
%     
%     
%     onTimes=onTimesRem;
% end













