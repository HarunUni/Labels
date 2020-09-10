function clearLables(dir)
%clearLables searches for overlapping lables and fixes them

% Check size of the timetable (TT)

disp('Loading File ...');
file = load(dir);
signalName = file.gTruth.DataSource.SignalName;
TT = file.gTruth.ROILabelData.(signalName);
frameNumber = size(TT, 1);
peopleNumber = size(TT, 2);

% Read the TT till finding overlapping lables, then delete the first one
% because it is the earlier or rather the overlapped one

disp('Searching ...');
for column = 1:peopleNumber
    for row = 1:frameNumber
        data = TT.(column)(row); % get the coordinate as an Array
        sizeOfData = size(data{1}, 1); % get the size of the array
    
        if sizeOfData >= 2
            disp(['Found in: ', int2str(row)]);
            data{1} = data{1}(end, :);
            
            TT.(column)(row) = data;
            
        end
    end
end

% Checking for Errors
disp('Checking for Errors')
for col = 1:size(TT, 2)
    for row = 1:size(TT, 1)
        if(size(TT{row, col}{1}, 2) ~= 4)
            disp(["Error in: row: ", int2str(row), " col: ", int2str(col)])
        end
    end
end

disp('Saving file ...');

% Creating a new GroundTruth Data to store the TT in it
gTruth = groundTruth(groundTruthDataSource(file.gTruth.DataSource.SourceName), file.gTruth.LabelDefinitions(1:2:end, [1, 3]), TT);
newFilename = "new " + dir;
save(newFilename, "gTruth");

msgbox(['Finished and saved as ', newFilename], 'Success');

end