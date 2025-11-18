# application/analytics/wordcloud_generator.py
from wordcloud import WordCloud

class WordCloudGenerator:
    def generate(self, messages, out_path, width=800, height=400):
        text = ' '.join(str(m.get('content','')) for m in messages if m.get('content'))
        if not text.strip():
            raise ValueError('No text to generate wordcloud')
        wc = WordCloud(width=width, height=height)
        img = wc.generate(text)
        img.to_file(out_path)
        return out_path