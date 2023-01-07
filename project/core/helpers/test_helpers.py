from django.urls import reverse


def login_rediretion(client, url_name, *args, **kwargs):
        login_url = reverse('users:login')
        url = reverse(url_name, **kwargs)
        response = client.get(url)

        assert response.url == '{login_url}?next={url}'.format(
            login_url=login_url, url=url)
