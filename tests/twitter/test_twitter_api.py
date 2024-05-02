def test_post_twitter(twitter_client):
    twitter_client.create_tweet(text="Hello, world!")


def make_tweet_text(gpt_client, messages):
    completion = gpt_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
    )

    return completion.choices[0].message.content


def test_post_gpt_twitter(gpt_client, twitter_client, messages):
    text = make_tweet_text(gpt_client, messages)

    twitter_client.create_tweet(text=text)
