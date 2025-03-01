from pyrogram import Client as Clients  # type: ignore


def create_pyrogram(name: str, **args):
    return Clients(name, **args)
