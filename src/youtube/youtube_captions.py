from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from pytube import YouTube as youtube
from youtube_transcript_api.formatters import JSONFormatter


class YtService:
    def __init__(self, id=None) -> None:
        self.video_id = id
        self.base_url = "https://www.youtube.com/watch?v="

    def getSrtCaption(self, video_id, target="en"):
        """
        Returns either a caption or a subtitle
        depenends on target language
        """
        url = self.base_url + video_id
        yt = youtube(url)
        captions = yt.captions
        if not captions.get(target):
            target = "a." + target  # get auto generated caption
        try:
            caption = yt.captions.get_by_language_code(target)
            xm_caption = caption.xml_captions
            srt_caption = caption.generate_srt_captions()
            return srt_caption
        except Exception as e:
            raise e

    def writeFile(self, content, output_dir):
        try:
            f = open(output_dir, "w", encoding='utf-8')
            f.write(content)
            f.close()
        except Exception as e:
            raise e

    def downloadVideo(self, video_id, output_dir, filename):
        url = self.base_url + video_id
        yt = youtube(url)
        try:
            print("downloading youtube video...")
            video = yt.streams.filter(progressive=True, file_extension="mp4")
            video.get_highest_resolution().download(
                filename=filename, output_path=output_dir
            )
            print("finished downloading.")
            return True
        except Exception as e:
            raise e

    def getSubtitleVideo(self, sub, font=None) -> SubtitlesClip:
        try:
            generator = lambda txt: TextClip(
                txt, font="Georgia-Regular", fontsize=40, color="yellow", bg_color="black"
            )
            subtitle = SubtitlesClip(sub, generator)
            return subtitle
        except Exception as e:
            raise e

    def getTranslation(self, video_id, src = "en",target="ar"):
        # retrieve the available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript([src])
        translated_transcript = transcript.translate(target)
        formatter = JSONFormatter()
        # .format_transcript(transcript) turns the transcript into a JSON string.
        print(translated_transcript.fetch())
        json_formatted = formatter.format_transcript(translated_transcript.fetch())
        # Now we can write it out to a file.
        with open('your_filename.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_formatted)

    def generateOutput(self, input_clip, sub_clip):
        try:
            # Overlay the text clip on the first video clip
            video = CompositeVideoClip([input_clip, sub_clip])
            # Write the result to a file
            video.write_videofile("youtube/output/output.mp4", fps=input_clip.fps)
        except Exception as e:
            raise e

