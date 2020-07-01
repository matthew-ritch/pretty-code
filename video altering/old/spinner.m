clc
clear
name='C:\Users\Matthew\Desktop\me+flan+fish';

im=imread([name '.jpg']);

n=6;


%do first normal
[r,c,~]=size(im);
len=200;

%spin
y{1}=im;
for i=2:len
    fact=floor(c/len);
y{i} = circshift(y{i-1},-fact,2); %circularly shifts the values in array A by K positions along dimension dim. 
%Inputs K and dim must be scalars.
end
ind=i;

%%shock
%divide indices
vec=[];
order=randperm(n);
for i=1:n
    vec=[vec,y{ind}(:,1+(order(i)-1)*round(c/n):min((order(i))*round(c/n),c),:)];
end
y{ind+1}=vec;
%spin
for i=ind+2:ind+len
    fact=floor(c/len);
y{i} = circshift(y{i-1},-fact,1); %circularly shifts the values in array A by K positions along dimension dim. 
%Inputs K and dim must be scalars.
end
ind=i;

%%shock
%divide indices
vec=[];
order=randperm(n);
for i=1:n
    vec=[vec;y{ind}(1+(order(i)-1)*round(r/n):min(order(i)*round(r/n),r),   :  ,:)];
end
y{ind+1}=vec;
%spin
for i=ind+2:ind+len
    fact=floor(c/len);
y{i} = circshift(y{i-1},-fact,2); %circularly shifts the values in array A by K positions along dimension dim. 
%Inputs K and dim must be scalars.
end
ind=i;

%%shock
%divide indices
vec=[];
order=randperm(n);
for i=1:n
    vec=[vec,y{ind}(:,1+(order(i)-1)*round(c/n):min((order(i))*round(c/n),c),:)];
end
y{ind+1}=vec;
%spin
for i=ind+2:ind+len
    fact=floor(c/len);
y{i} = circshift(y{i-1},-fact,1); %circularly shifts the values in array A by K positions along dimension dim. 
%Inputs K and dim must be scalars.
end
ind=i;

%%shock
%divide indices
vec=[];
order=randperm(n);
for i=1:n
    vec=[vec;y{ind}(1+(order(i)-1)*round(r/n):min(order(i)*round(r/n),r),   :  ,:)];
end
y{ind+1}=vec;
%spin
for i=ind+2:ind+len
    fact=floor(c/len);
y{i} = circshift(y{i-1},-fact,2); %circularly shifts the values in array A by K positions along dimension dim. 
%Inputs K and dim must be scalars.
end
ind=i;

%%shock
%divide indices
vec=[];
order=randperm(n);
for i=1:n
    vec=[vec,y{ind}(:,1+(order(i)-1)*round(c/n):min((order(i))*round(c/n),c),:)];
end
y{ind+1}=vec;
%spin
for i=ind+2:ind+len
    fact=floor(c/len);
y{i} = circshift(y{i-1},-fact,1); %circularly shifts the values in array A by K positions along dimension dim. 
%Inputs K and dim must be scalars.
end
ind=i;

%%shock
%divide indices
vec=[];
order=randperm(n);
for i=1:n
    vec=[vec;y{ind}(1+(order(i)-1)*round(r/n):min(order(i)*round(r/n),r),   :  ,:)];
end
y{ind+1}=vec;
%spin
for i=ind+2:ind+len
    fact=floor(c/len);
y{i} = circshift(y{i-1},-fact,2); %circularly shifts the values in array A by K positions along dimension dim. 
%Inputs K and dim must be scalars.
end
ind=i;

%%shock
%divide indices
vec=[];
order=randperm(n);
for i=1:n
    vec=[vec,y{ind}(:,1+(order(i)-1)*round(c/n):min((order(i))*round(c/n),c),:)];
end
y{ind+1}=vec;
%spin
for i=ind+2:ind+len
    fact=floor(c/len);
y{i} = circshift(y{i-1},-fact,1); %circularly shifts the values in array A by K positions along dimension dim. 
%Inputs K and dim must be scalars.
end
ind=i;

%%shock
%divide indices
vec=[];
order=randperm(n);
for i=1:n
    vec=[vec;y{ind}(1+(order(i)-1)*round(r/n):min(order(i)*round(r/n),r),   :  ,:)];
end
y{ind+1}=vec;
%spin
for i=ind+2:ind+len
    fact=floor(c/len);
y{i} = circshift(y{i-1},-fact,2); %circularly shifts the values in array A by K positions along dimension dim. 
%Inputs K and dim must be scalars.
end
ind=i;

%%shock
%divide indices
vec=[];
order=randperm(n);
for i=1:n
    vec=[vec,y{ind}(:,1+(order(i)-1)*round(c/n):min((order(i))*round(c/n),c),:)];
end
y{ind+1}=vec;
%spin
for i=ind+2:ind+len
    fact=floor(c/len);
y{i} = circshift(y{i-1},-fact,1); %circularly shifts the values in array A by K positions along dimension dim. 
%Inputs K and dim must be scalars.
end
ind=i;

%%shock
%divide indices
vec=[];
order=randperm(n);
for i=1:n
    vec=[vec;y{ind}(1+(order(i)-1)*round(r/n):min(order(i)*round(r/n),r),   :  ,:)];
end
y{ind+1}=vec;
%spin
for i=ind+2:ind+len
    fact=floor(c/len);
y{i} = circshift(y{i-1},-fact,2); %circularly shifts the values in array A by K positions along dimension dim. 
%Inputs K and dim must be scalars.
end
ind=i+1;


name=[name(1:end-4),'_spun'];
v1=VideoWriter(name,'MPEG-4');
v1.FrameRate=45;
open(v1);
nReps=1;
L=length(y);
for j=1:nReps
for i=1:L
    frame=y{i};
    
    writeVideo(v1,frame);
end
end

close(v1)