from moviepy.editor import *
import os
import glob
from datetime import date

images = [];
texts = [];

title = '';
level = '';

for file in glob.glob('input/*.*'):
    images.append(file);
    text = os.path.splitext(os.path.basename(file))[0]
    texts.append(text);

config = open('config.txt', 'r');
lines = config.readlines();
for line in lines:
    split = line.split(':', 1);
    if split[0] == 'TITLE':
        title = split[1];
    if split[0] == 'LEVEL':
        level = split[1];
        

#configuartions
title_duration = 2;
difficulty_duration = 2;
image_duration = 2.5;
next_image = 4;
text_duration = 1
font_size = 70
text_color = 'white'
closure_text = 'LET US KNOW\nYOUR SCORE';


video = VideoFileClip("background.mp4").subclip(0, 44);
#audio = AudioFileClip("audio.mp3");
taskList = [];

start_time = 0;
titleClip = ( TextClip(title, fontsize = 60,color='white', font='Arial', stroke_width=3, stroke_color='white')
             .set_position('center')
             .set_start(start_time)
             .set_duration(title_duration) );
start_time = start_time + title_duration;

difficultyClip = ( TextClip(level, fontsize = 60,color='white', font='Courier', stroke_width=3, stroke_color='white')
             .set_position('center')
             .set_start(start_time)
             .set_duration(difficulty_duration) );
start_time = start_time + difficulty_duration;

taskList.append(video);
taskList.append(titleClip);
taskList.append(difficultyClip);

#add a 1s delay
start_time = start_time + 1;

temp_start_time = start_time;
#adding images
count = 1;
for image in images:
    image_clip = ImageClip(image).set_start(start_time).set_duration(image_duration).set_pos(("center","center"))
    count_clip = ( TextClip("#" + str(count), fontsize = 60,color='white', font='Courier', stroke_width=3, stroke_color='white')
             .set_position((0.45, 0.7), relative=True)
             .set_start(start_time)
             .set_duration(image_duration) );
    start_time = start_time + next_image;
    taskList.append(image_clip);
    taskList.append(count_clip);
    count = count + 1;

#reverting start time for text
start_time = temp_start_time + image_duration;
#add 0.5 delay after the image is shown
start_time = start_time + 0.5;

#adding texts
for text in texts:
    txt_clip = ( TextClip(text,fontsize = font_size,color=text_color, font='Courier',stroke_width=3, stroke_color='white')
             .set_position('center')
             .set_start(start_time)
             .set_duration(text_duration) )
    taskList.append(txt_clip);
    start_time = start_time + next_image;


#add a delay
start_time = start_time - next_image + 2.5;
#add the closure
closure_text = ( TextClip(closure_text,fontsize = 70,color=text_color, font='Courier',stroke_width=3, stroke_color='white')
             .set_position('center')
             .set_start(start_time)
             .set_duration(3) )

taskList.append(closure_text);

result = CompositeVideoClip(taskList);
#result.audio = audio;
today = date.today()
file_name = "output/" + str(today) + ".mp4";
result.write_videofile(file_name,fps=25)