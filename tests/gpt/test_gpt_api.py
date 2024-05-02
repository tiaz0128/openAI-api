def test_openai_api(gpt_client, messages):
    completion = gpt_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
    )

    assert completion.choices[0].message.content

    with open(".temp/output.txt", "w") as f:
        f.write(completion.choices[0].message.content)
