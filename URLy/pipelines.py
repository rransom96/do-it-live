from django.shortcuts import render_to_response
from social.pipeline.partial import partial


@partial
def pick_character_name(backend, details, response, is_new=False, *args, **kwargs):
    if backend.name == 'battlenet-oauth2' and is_new:
        data = backend.strategy.request_data()
        if data.get('character_name') is None:
            # New user and didn't pick a character name yet, so we render
            # and send a form to pick one. The form must do a POST/GET
            # request to the same URL (/complete/battlenet-oauth2/). In this
            # example we expect the user option under the key:
            #   character_name
            # you have to filter the result list according to your needs.
            # In this example, only guild members are allowed to sign up.
            char_list = [
                c['name'] for c in backend.get_characters(response.get('access_token'))
                    if 'guild' in c and c['guild'] == '<guild name>'
            ]
            return render_to_response('pick_character_form.html', {'charlist': char_list, })
        else:
            # The user selected a character name
            return {'username': data.get('character_name')}