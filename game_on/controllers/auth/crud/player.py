import cherrypy

from game_on import database as db
from game_on import games
from game_on.controllers.auth.crud import base_crud

class PlayerCrud(base_crud.BaseCrud):
    db = db
    model = db.Player
    readonly_properties = ['uuid', 'creator_uuid']

    def can_write(self, user, obj):
        """
        Does the user have write access to this resource?
        """
        return obj.creator is None or obj.creator == user

    def get_form_data(self, obj):
        #Get default form properties
        form_data = super(PlayerCrud, self).get_form_data(obj)

        #Override form properties
        for prop in form_data:
            #Change game to be a list of options
            if prop['name'] == 'game':
                prop['type'] = 'Related'

                options = []
                for game in games.get_games().keys():
                    options.append({
                        'label': game,
                        'value': game,
                    })
                prop['options'] = options

            #Show a value for creator
            if prop['name'] == 'creator_uuid':
                prop['value'] = cherrypy.request.user.name

        #Add extra form properties
        form_data.append({
            'label': 'File',
            'name': 'file',
            'type': 'File',
            'readonly': False,
        })

        return form_data

    def set_form_data(self, obj, data):
        #Deal with non-form properties
        obj.creator = cherrypy.request.user

        #Remove the extra form properties
        player_file = data.pop('file', None)

        #Deal with default form properties
        validation_errors = super(PlayerCrud, self).set_form_data(obj, data)

        #Deal with extra form properties
        if player_file.length:
            #Save the file to disk
            raise Exception('TODO: Save player file')
        elif not obj.uuid:
            validation_errors.append('You must upload a file when creating a Player.')

        return validation_errors


def mount_tree():
    return PlayerCrud()
