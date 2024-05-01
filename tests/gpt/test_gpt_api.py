from openai import OpenAI


def test_openai_api(api_key):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "질문에 대한 답변은 항상 한 문장으로 작성해주세요.",
            },
            {
                "role": "user",
                "content": "위키북스에 대해서 아는데 말해줘.",
            },
        ],
        max_tokens=100,
    )

    assert completion.choices[0].message.content

    with open(".temp/output.txt", "w") as f:
        f.write(completion.choices[0].message.content)
