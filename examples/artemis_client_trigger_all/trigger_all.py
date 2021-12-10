"""Triggers every participation of a programming exercise.

This is a workaround for an Artemis bug that stops triggering exercises
when using the "Trigger All" button in the Artemis-UI.
"""

import artemis_client
from artemis_client.api import Exercise
from aiohttp.client_exceptions import ClientResponseError
import getpass
import asyncio
import os
from itertools import islice
from simple_term_menu import TerminalMenu


def clear():
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')


clear()
username = input("Username: ")
password = getpass.getpass("Password: ")
artemis_url = input("Artemis URL: ")


async def main():
    async with artemis_client.ArtemisSession(
        artemis_url, username, password
    ) as session:

        clear()
        courses = [x async for x in session.course.get_courses()]
        print("Select course:")
        menu = TerminalMenu([f"{c['id']} {c['title']}" for c in courses])
        course = courses[menu.show()]  # type: ignore

        clear()
        exercises = [x async for x in session.course.get_exercises_for_course(course["id"]) if x["type"] == "programming"]
        print("Select exercise")
        menu = TerminalMenu([f"{e['id']} {e['title']}" for e in exercises])
        exercise: Exercise = exercises[menu.show()]  # type: ignore

        clear()
        participations = [x async for x in session.exercise.get_participations(exercise["id"])]
        piter = iter(participations)

        # While the artemis_client is able to perform parallel requests
        # we do not do this here to prevent flooding the build queue.
        while True:
            chunk = list(islice(piter, 10))
            for p in chunk:
                print(f"Trigger participation for {p['participantIdentifier']}...", end="")
                try:
                    await session.submission.programming.trigger_build(p)
                    print("ok")
                except ClientResponseError as e:
                    print("FAIL" + str(e))
            if not chunk:
                break
            print("\nGiving Artemis 5s to recover...\n")
            await asyncio.sleep(5)

asyncio.run(main())
