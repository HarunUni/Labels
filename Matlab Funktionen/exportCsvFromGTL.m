function exportCsvFromGTL(GTLFile)
%exportCsvFromGTR Export a csv table from the exported GTL file

disp("Loading File ...")
file = load(GTLFile);
TT = file.gTruth.LabelData;
variableNames = string(TT.Properties.VariableNames);
str = string(uint16(cell2mat(TT.Variables)));
prefix = '"[';
postfix = ']"';

str(:, 1:4:size(str,2)) = append(prefix, str(:, 1:4:size(str,2)));
str(:, 4:4:size(str,2)) = append(str(:, 4:4:size(str,2)), postfix);

disp("Saving File ...")
fname = GTLFile + " CSV.csv";
fopen(fname, 'a');

writematrix(variableNames, fname);
writematrix(str, fname, 'WriteMode', 'append');

fclose('all');

end
