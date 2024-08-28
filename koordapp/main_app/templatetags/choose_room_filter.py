from django import template

register = template.Library()


@register.filter
def is_occupied(rooms, room):
    #filter ob in aktueller Zeit   
    if(rooms.filter(raum = room).exists()):
        return True
    return False