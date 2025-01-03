import random

from psychopy.colors import Color
import pandas as pd
import random

class writtingprt:
    def __init__(self):
        self.colors_list = ["255 255 51", "0 255 0", "51 51 255", "255 51 255", "102 255 255", "255 102 178", "255 153 51",
                       "0 204 204", "255 153 153"]

        self.colors_list1 = ["255 255 51", "0 255 0", "51 51 255", "255 51 255", "102 255 255", "255 102 178", "255 153 51",
                        "0 204 204", "255 153 153"]


    def random_color(self):
        if self.colors_list != []:
            result = random.choice(self.colors_list)
            self.colors_list.remove(result)
            return result
        else:
            return random.choice(self.colors_list1)
    def create_experiment_file(self,filename,basics):
        with open(filename, 'w') as file:
            colors_list = ["255 255 51", "0 255 0", "51 51 255", "255 51 255", "102 255 255", "255 102 178", "255 153 51",
                           "0 204 204", "255 153 153"]
            backgroundcolor = self.random_color()
            self.colors_list1.remove(backgroundcolor)
            result = basics.get("result")
            file.write("\nFileVersion:        2\n\n")
            file.write("ResolutionOfTime:   msec\n\n")
            file.write("Experiment:         prt\n\n")

            file.write("BackgroundColor:    "+backgroundcolor+"\n")
            file.write("TextColor:          255 255 255\n\n")
            file.write("TimeCourseColor:    255 255 255\n")
            file.write("TimeCourseThick:    3\n")
            file.write("ReferenceFuncColor: 192 192 192\n")
            file.write("ReferenceFuncThick: 2\n\n")
            file.write("NrOfConditions:     "+str(len(result))+"\n\n")

            for x in result:
                file.write(x+"\n")
                file.write(str(result.get(x).get("count"))+"\n")
                for y in range(len(result.get(x).get("onsets"))):
                    file.write("  "+str(result.get(x).get("onsets")[y]) + " " + str(result.get(x).get("endsets")[y]) + "\n")
                file.write("Color: "+ self.random_color() +"\n\n")



    def psychopy_to_rgb(self,psychopy_color):
        rgbs = []
        for component in psychopy_color:
            rgbs.append(int(((component+1) /2) *255))
        tostring = []
        for value in rgbs:
            tostring.append(str(value))
        tostring = " ".join(tostring)
        return tostring




    def analyze_trial_types(self, csv_file, col="trial_type", min_gap=1):
        df = pd.read_csv(csv_file, delimiter=";")

        df['onset'] = pd.to_numeric(df['onset'], errors='coerce')
        df['duration'] = pd.to_numeric(df['duration'], errors='coerce')

        df['onset'] = df['onset'].fillna(0).astype(int)
        df['duration'] = df['duration'].fillna(0).astype(int)
        trial_type_data = {}

        for trial_type in df[col].unique():
            if trial_type != 'Fixation':
                filtered_df = df[df[col] == trial_type]
                count = len(filtered_df)
                onsets = filtered_df['onset'].tolist()
                durations = filtered_df['duration'].tolist()
                endsets = (filtered_df['onset'] + filtered_df['duration']).tolist()

                for i in range(1, len(onsets)):
                    if onsets[i] < endsets[i - 1]:
                        onsets[i] = endsets[i - 1]
                    endsets[i] = onsets[i] + durations[i]

                trial_type_data[trial_type] = {
                    "count": count,
                    "onsets": onsets,
                    "durations": durations,
                    "endsets": endsets
                }

        if 'Fixation' in df[col].unique():
            fixation_df = df[df[col] == 'Fixation']
            onsets = fixation_df['onset'].tolist()
            durations = fixation_df['duration'].tolist()
            endsets = (fixation_df['onset'] + fixation_df['duration']).tolist()

            for i in range(1, len(onsets)):
                if onsets[i] < endsets[i - 1]:
                    onsets[i] = endsets[i - 1]
                endsets[i] = onsets[i] + durations[i]
            trial_type_data['Fixation'] = {
                "count": len(fixation_df),
                "onsets": fixation_df['onset'].tolist(),
                "durations": fixation_df['duration'].tolist(),
                "endsets": endsets
            }

        return trial_type_data

    def adjust_onsets_to_start_at_zero(self,trial_type_data):
        min_onset = None
        min_trial_type = None

        for trial_type in trial_type_data:
            onsets = trial_type_data[trial_type]["onsets"]
            current_min_onset = min(onsets)
            if min_onset is None or current_min_onset < min_onset:
                min_onset = current_min_onset
                min_trial_type = trial_type

        if min_onset is not None and min_trial_type is not None:
            trial_type_data[min_trial_type]["onsets"][0] = 0
        return trial_type_data


