from .models import  User

def logout(request):
    try:
        u = User.objects.get(user = request.session['usuario'])
    except:
        pass
    else:
        if u.logoutuser():
            u.login = False
            u.save()
            request.session.pop('usuario')


def huser(request) -> bool:
    if 'usuario' in request.session:
        return True
    return False
