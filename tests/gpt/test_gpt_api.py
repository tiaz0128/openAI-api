from openai import OpenAI


def test_openai_api(api_key):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
            },
            {
                "role": "user",
                "content": "Compose a poem that explains the concept of recursion in programming.",
            },
        ],
    )

    with open(".temp/output.txt", "w") as f:
        f.write(completion.choices[0].message.content)
