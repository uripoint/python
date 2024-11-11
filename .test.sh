
# ffmpeg -i "rtsp://test1234:test1234@192.168.188.225:554/Preview_01_sub" -vf "format=rgb24,dlopen=esrgan.so:upscale:model=$3/ESRGAN.pb,scale=3840:2160:flags=lanczos" -c:v libx264 -preset slower -crf 20 -c:a copy -f segment -segment_time 300 -strftime 1 recognition/upscaled.mp4

 ffmpeg -i rtsp://test1234:test1234@192.168.188.225:554/Preview_01_sub -vf "format=rgb24,dlopen=recognition.so:detect:model=model://recognition/model.pb:labels=model://recognition/labels.txt,drawbox=enable='between(t,td_start,td_end)':x='xd':y='yd':w='wd':h='hd':color=yellow:thickness=2" -c:v libx264 -preset fast -crf 23 -f segment -segment_time 300 -strftime 1 ./recognition/tracked.mp4

ffmpeg -i rtsp://test1234:test1234@192.168.188.225:554/Preview_01_sub \
  -vf "format=rgb24,\
       dlopen=./recognition/recognition.so:detect:\
       model=./recognition/model.pb:\
       labels=./recognitionlabels.txt,\
       drawbox=enable='between(t,\${td_start},\${td_end})':\
       x=\${xd}:y=\${yd}:w=\${wd}:h=\${hd}:\
       color=yellow:thickness=2" \
  -c:v libx264 -preset fast -crf 23 \
  -f segment -segment_time 300 -strftime 1 \
  ./recognition/tracked.mp4
