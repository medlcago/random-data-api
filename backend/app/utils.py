from faker import Faker


class UserUtil:
    @staticmethod
    def _generate_user_info(locale: str | None = None):
        fake = Faker(locale=locale)

        name = fake.name()
        address = fake.address()
        email = fake.email()
        phone_number = fake.phone_number()
        username = fake.user_name()
        password = fake.password(length=20)
        job = fake.job()

        user_info = {
            "name": name,
            "address": address,
            "email": email,
            "phone_number": phone_number,
            "username": username,
            "password": password,
            "job": job,
        }

        return user_info

    @staticmethod
    def _generate_user_profile(locale: str | None = None, simple: bool = True):
        fake = Faker(locale=locale)

        if simple:
            return fake.simple_profile()
        return fake.profile()

    def generate_user_profile(self, locale: str | None = None, n: int = 1, simple: bool = True):
        if n == 1:
            return self._generate_user_profile(locale=locale, simple=simple)
        return [self._generate_user_profile(locale=locale, simple=simple) for _ in range(n)]

    def generate_user_info(self, locale: str | None = None, n: int = 1):
        if n == 1:
            return self._generate_user_info(locale=locale)
        return [self._generate_user_info(locale=locale) for _ in range(n)]
