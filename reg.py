from mastodon import Mastodon


Mastodon.create_app(
    'fluxpost',
    api_base_url = 'https://ioc.exchange',
    to_file = 'clientcred.secret'
)
