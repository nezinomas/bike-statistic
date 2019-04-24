from django.urls import reverse


def login_rediretion(client, url_name):
        login_url = reverse('accounts:login')
        url = reverse(url_name)
        response = client.get(url)

        assert response.url == '{login_url}?next={url}'.format(
            login_url=login_url, url=url)
