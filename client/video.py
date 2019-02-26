'''
video module
'''

from subprocess import call


def stream(candidate = "127.0.0.1:8000", webcam = "video0", audio = "1", audioBitrate = "64K", videoSize = "640*360", videoBitrate = "373K"):
    '''
    stream to remote client
    '''

    #-loglevel panic

    # ffmpeg -i /media/jimmy/HD-PZU3/VEDIO/12St.80.wdl/12.Strong.2018.1080p.WEB-DL.mkv -acodec libmp3lame -b:a 384k -async 1 -c:v libx265 -s 1920*1080 -crf 28 -b:v 8000k -f mpegts udp://127.0.0.1:5000

    ffmpeg_cmd = ("ffmpeg -f v4l2 -i /dev/%s -f alsa -ac 2 -i hw:%s \
                          -acodec libmp3lame \
                          -b:a %s \
                          -async 1 \
                          -c:v libx265 \
                          -s %s \
                          -crf 28 \
                          -b:v %s \
                          -preset ultrafast \
                          -f mpegts udp://%s?pkt_size=1316" 
                          % (webcam, audio, audioBitrate, videoSize, videoBitrate, candidate)).split()

    try:
        _ = call(ffmpeg_cmd)
    except KeyboardInterrupt:
        print("LOG: RTC stop")
    except:
        print("ERROR: Video stream error")
        exit()

def show_remote_cam(local_ip):
    '''
    display remote video
    '''

    vlc_cmd = ("vlc udp://@%s" % local_ip).split()

    try:
        _ = call(vlc_cmd)
    except:
        print("ERROR: VLC error")
        exit()