function gTruth = ImportDataGTL(coordinatesFile, infoFile)
%IMPORT_DATA_GTL Importing The Coordintes and additional information from
%the labeling Algorithm to the GroundTruthLabeler (GTL)

disp('Opening Files...')
info = readtable(infoFile);
coordinates = readtable(coordinatesFile, 'Delimiter', ',');
arraySize = info.number_of_person; % + info.poss_wrong_det;

% Preallocatiing Memory
lables{info.frame_count} = 0;
allLables{arraySize} = 0;
types{arraySize} = 0;
defs{arraySize} = 0;
people{arraySize} = 0;

disp('Reading data...')
for person = 1:arraySize
    types{person} = 'Rectangle';
    defs{person} = '"';
    people{person} = strcat('Person_', num2str(person));
    
    for frame = 1:info.frame_count
        lables{frame} = reshape(str2double(regexp(coordinates{frame, person}{1},'\d*','match')), 1,4);
    end
    
    allLables{person} = lables';
end

allTypes = labelType(types');

% Data Source
gtSource = groundTruthDataSource(info.video_source{1});

% Label Definitions
varNames = {'Name', 'Type', 'Description'};
lblDef = table(people', allTypes, defs', 'VariableNames', varNames);

% Label Data
timeOfVideoSec = info.time_of_video / 1000;
time = linspace(seconds(0), seconds(timeOfVideoSec), info.frame_count);
TT = timetable(time', allLables{:}, 'VariableNames', people);

% Creating the GroundTruth File
disp('Creating the GroundTruth File...')
gTruth = groundTruth(gtSource, lblDef, TT);

end