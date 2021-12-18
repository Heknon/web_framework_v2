import jwt


class JwtSecurity:
    SECRET = "secret_key"

    @staticmethod
    def token_factory():
        def decorator(fun):
            setattr(fun, "jwt_security_factory", {
                "create_token": JwtSecurity.create_token
            })
            return fun

        return decorator

    @staticmethod
    def create_token(request):
        # DB VERIFY
        return jwt.encode({
            "username": request.body.username
        }, JwtSecurity.SECRET)

    @staticmethod
    def token_auth(check_blacklist: bool):
        def decorator(fun):
            setattr(fun, "jwt_security_factory", {
                "authenticate_token": JwtSecurity.authenticate_token,
                "check_blacklist": JwtSecurity.check_blacklist if check_blacklist else None
            })
            return fun

        return decorator

    @staticmethod
    def authenticate_token(request):
        try:
            jwt.decode(request.headers["Authorization"][7:], JwtSecurity.SECRET, algorithms=["HS256"])
            return True
        except:
            return False

    @staticmethod
    def check_blacklist() -> bool:
        return None
