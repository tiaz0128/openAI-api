import pytest


class TestWhisper:
    @pytest.fixture(autouse=True)
    def setup(self, gpt_client, wave_file, transcript):
        self.gpt_client = gpt_client
        self.wave_file = wave_file

        self.transcript = transcript

    def test_translate(self):
        transcript = self.gpt_client.audio.translations.create(
            model="whisper-1",
            file=self.wave_file,
        )

        with open(".temp/translations.txt", "w") as f:
            f.write(transcript.text)

    def test_transcript(self):
        transcript = self.gpt_client.audio.transcriptions.create(
            model="whisper-1",
            file=self.wave_file,
        )
        with open(".temp/transcriptions.txt", "w") as f:
            f.write(transcript.text)

    def test_translate_with_summary_messages(self):
        messages = [
            {
                "role": "user",
                "content": f"다음 문장을 한국어로 번역하고 3줄의 글머리 기호로 요약하세요: \n{self.transcript}",
            },
        ]

        summary = self.gpt_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        with open(".temp/summary.txt", "w") as f:
            f.write(summary.choices[0].message.content)
