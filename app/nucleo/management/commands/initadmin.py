import logging
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Command(createsuperuser.Command):
    """
    Command for create superuser with password arg.

    Fail silent if user already exist.
    """

    help = "Create a superuser with a password"

    def add_arguments(self, parser):
        """
        Add optional argument for handle password.
        """
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            "--password",
            dest="password",
            default=None,
            help="Specifies the password for the superuser.",
        )

    def handle(self, *args, **kwargs):
        password = kwargs.get("password")
        username = kwargs.get("username")
        database = kwargs.get("database")

        if password and not username:
            raise CommandError(
                "--username is required if specifying --password"
            )

        try:
            # Create superuser
            super(Command, self).handle(*args, **kwargs)

            # Set password
            db_manager = self.UserModel._default_manager.db_manager(database)
            user = db_manager.get(username=username)
            if password:
                user.set_password(password)
                user.save()

        except CommandError as e:
            logger.debug(e)
