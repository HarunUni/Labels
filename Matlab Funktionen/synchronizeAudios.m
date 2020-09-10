function synchronizeAudios(cam, vorne, hinten, links, rechts, LL, RR, LM, LR)
%SYNCHRONIZEAUDIOS Shift all audios so that they are synchronized
% Usage: "Kamera Audio.wav", "Hinten.wav", "Links.wav", "LL.wav", "LM.wav", "LR.wav", "Mixdown.wav", "Rechts.wav", "RR.wav", "Vorne.wav"

sr = 16e3;
disp("Reading")
array = [vorne, hinten, links, rechts];
kinect = [LL, RR, LM, LR];
dir = [array, kinect];

%% Reading Camera Audio

cam_Duration = audioinfo(cam).Duration;

[y_cam, sr_cam] = audioread(cam);
if size(y_cam, 2) >= 2
    y_cam = y_cam(:, 1);
end

if sr_cam ~= sr
    y_cam = resample(y_cam, sr, sr_cam);
    y_cam = y_cam(1:end-1);
    samples = uint32(cam_Duration*sr)-1;
else
    samples = uint32(cam_Duration * sr);
end

audios = zeros(samples, length(dir));


%% Reading Reference Audio from the Microphone-array and Kinect

arr_ref = vorne;  % here I choose "vorne" as the reference for the array

[y_arr, sr_arr] = audioread(arr_ref);  
if size(y_arr, 2) >= 2
    y_arr = y_arr(:, 1);
end

if sr_arr ~= sr
    y_arr = resample(y_arr, sr, sr_arr);
    y_arr = y_arr(1:end-1);
end

kin_ref = LL;  % here I choose "LL as the reference for the kinect
[y_kin, sr_kin] = audioread(kin_ref);
if size(y_kin, 2) >= 2
    y_kin = y_kin(:, 1);
end

if sr_kin ~= sr
    y_kin = resample(y_kin, sr, sr_kin);
    y_kin = y_kin(1:end-1);
end

%% Calculating the delays between the array and kinect to the camera 

% for the array
[cc, lags] = xcorr(y_cam, y_arr);
[~, maximum] = max(cc);
arr_delay = int32(maximum - find(lags == 0));

% for the kinect
[cc, lags] = xcorr(y_cam, y_kin);
[~, maximum] = max(cc);
kin_delay = int32(maximum - find(lags == 0));


delays = ["Array", num2str(arr_delay) + " samples"; "Kinect", num2str(kin_delay) + " samples"];


%% Shifting all the audios to camera audio

for i = 1:length(dir)
    name = dir(i);
    disp(name)
    
    if name ~= kin_ref || name ~= arr_ref
         [y, sr_audio] = audioread(name); % read the audio
    elseif name == kin_ref
        y = y_kin;
        sr_audio = sr_kin;
    elseif name == arr_ref
        y = y_arr;
        sr_audio = sr_arr;
    end
    
    if size(y, 2) >= 2 % if the audio has more channels than one, than take the first one
        y = y(:, 1);
    end
    
    if sr_audio ~= sr
        y = resample(y, sr, sr_audio);
        y = y(1:end-1);
    end
    
    if ismember(name, array)
        y = circshift(y, arr_delay);
        y = y(1:length(y_cam));
        
    else
        y = circshift(y, kin_delay);
        y = y(1:length(y_cam));
    end
    
    % fix the length if the difference is only 1
    if abs(length(y) - samples) == 1
        
        y = y(1:end-1);
    
    end
    
    audios(:, i) = y;
end

%% Saving all the audios and delays
disp('Saving...')
mkdir('new Audios');

audiowrite("new Audios/new " + cam, y_cam, sr);

for i = 1:length(dir)
    name = audios(:, i);
    audiowrite("new Audios/new " + dir(i), name, sr);
end

writematrix(delays, "new Audios/delays.txt");

extra_info = ["Samplerate", num2str(sr); "Reference Array", arr_ref; "Reference Kinect", kin_ref];

writematrix(extra_info, "new Audios/delays.txt", "WriteMode", "append");

end
