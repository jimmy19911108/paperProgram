'''
video module
'''

from subprocess import call


def stream(candidate = "127.0.0.1:8000", webcam = "video0", audio = "0", audioBitrate = "64K", videoSize = "640*360", videoBitrate = "373K"):
    '''
    stream to remote client
    '''

    #-loglevel panic

    ffmpeg_cmd = ("ffmpeg -f v4l2 -i /dev/%s -f alsa -ac 2 -i hw:%s \
    -acodec libmp3lame -b:a %s -async 1 -c:v libx265 -s %s -crf 28 -b:v %s -f mpegts udp://%s"\
    % (webcam, audio, audioBitrate, videoSize, videoBitrate, candidate)).split()

    try:
        p = call(ffmpeg_cmd)
    except KeyboardInterrupt:
        print("LOG: RTC stop")
    except:
        print("ERROR: Video stream error")
        exit()

def show_remote_cam(local_ip):
    '''
    display remote video
    '''

    print("local ip: %s" % local_ip)
    vlc_cmd = ("vlc udp://@%s" % local_ip).split()

    try:
        p = call(vlc_cmd)
    except:
        print("ERROR: VLC error")
        exit()