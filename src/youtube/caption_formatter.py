from youtube_transcript_api.formatters import Formatter

class CaptionFormatter(Formatter):
    def format_transcript(self, transcript, **kwargs):
        # Do your custom work in here, but return a string.
        return 'your processed output data as a string.'

    def format_transcripts(self, transcripts, **kwargs):
        # Do your custom work in here to format a list of transcripts, but return a string.
        return 'your processed output data as a string.'
