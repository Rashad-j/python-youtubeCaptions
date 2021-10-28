from youtube.youtube_captions import YtService
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import VideoFileClip

if __name__ == "__main__":
    video_id = "PM101DvvG4Q"
    input_dir = "youtube/input/"
    srt_file = "youtube/output/sub.srt"
    caption_target = "en"
    input_video = "input.mp4"
    # download the video
    try:
        sub_obj = YtService()
        sub_obj.downloadVideo(video_id, input_dir, "input.mp4")
        # get the subtitle/caption
        srt_caption = sub_obj.getSrtCaption(video_id)
        # save captions to a file
        sub_obj.writeFile(srt_caption, srt_file)
        # get the input clip 
        input_clip = VideoFileClip(input_dir + input_video)
        clip_x, clip_y = input_clip.size
        # get the captions in SubtitlesClip
        subtitle_clip = sub_obj.getSubtitleVideo(srt_file)
        subtitle_clip.size = (clip_x, 100)
        subtitle_clip = subtitle_clip.set_duration(input_clip.duration)
        subtitle_clip = subtitle_clip.set_position(("center", "bottom"))
        # save the output file
        sub_obj.generateOutput(input_clip, subtitle_clip)

    except Exception as e:
        print("There was a problem: " , e)
    