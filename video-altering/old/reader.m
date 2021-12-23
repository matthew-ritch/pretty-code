clc
clear
close all
%name='20190126_170929.mp4';
%name='20190126_172012.mp4';
%name='video-1549862734.mp4';
name='20150923_215753.mp4';
v=VideoReader(name);
frames=[];
i=1;
factor=9;
nReps=1;
while hasFrame(v)
    frames{i}=readFrame(v);
    i=i+1;
    %imshow(frames{i-1});
end
%frames(41:end)=[];
%frames(21:40)=[];
L=length(frames);
[r,c,~]=size(frames{1});
frames{end}=frames{end-1};
save=frames;
tVec=0:(L/factor):L;

%split into portions

% for i=1:factor
%     for j=1:length(frames)
%         splits{i,j}=frames{1+round(mod(j+tVec(i),L))}   (1+mod((i-1),2)*(r/sqrt(factor))  :  mod((i-1),2)*(r/sqrt(factor)), (1+(i-1)*(c/sqrt(factor))  :  (i)*(c/sqrt(factor))),:);
%     end
% end

for i=1:L
    %step thru all rows
   for j=1:sqrt(factor)
       %step thru all cols
   for k=1:sqrt(factor)
       sqVal=k+(j-1)*sqrt(factor);
       %set time for tile start
       tOffset=round(mod(tVec(sqVal),L));
       %current time
       t=1+mod(i+tOffset,L);
       %slice
       cStart=1+(k-1)*c/sqrt(factor);
       cEnd=(k)*c/sqrt(factor);
       rStart=1+(j-1)*r/sqrt(factor);
       rEnd=(j)*r/sqrt(factor);
       
       %set split
       splits{i,j,k}=frames{t}(rStart:rEnd,cStart:cEnd,:);
   end
   
   end
end

for i=1:L
    
        rows=[];
        for j=1:sqrt(factor)
            %do each column
            cols=[];
            for k=1:sqrt(factor)
                cols=[cols,splits{i,j,k}];
            end
            rows=[rows;cols];
        end
        outFrames{i}=rows;

end

name=[name(1:end-4),'_tiledStagger'];
v1=VideoWriter(name,'MPEG-4');
v1.FrameRate=27;
open(v1);

for j=1:nReps
for i=1:L
    frame=outFrames{i};
    
    writeVideo(v1,frame);
end
end

close(v1)